const $ = (selector) => document.querySelector(selector);
const state = { mode: 'demo', config: null, aoi: null, map: null, layers: {}, observations: [], detections: [], analysis: null, timelineTimer: null, truckMap: null, threeRenderer: null, threeFrame: null };

function escapeHtml(value) { return String(value ?? '').replace(/[&<>'"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' })[char]); }
async function api(url, options = {}) {
  const response = await fetch(url, options);
  let payload = null;
  try { payload = await response.json(); } catch { /* Download responses are intentionally not JSON. */ }
  if (!response.ok) throw new Error(payload?.detail || 'This operation could not be completed.');
  return payload;
}
function notify(message, type = '') { const notice = $('#notice'); notice.textContent = message; notice.className = `notice ${type}`; }
function formatDate(value) { return value ? new Date(`${value}T12:00:00`).toLocaleDateString(undefined, { day: '2-digit', month: 'short', year: 'numeric' }) : '—'; }
function setClock() { $('#clock').textContent = new Intl.DateTimeFormat(undefined, { dateStyle: 'medium', timeStyle: 'short' }).format(new Date()); }
function kpi(label, value, color = '') { return `<div class="kpi ${color}"><small>${escapeHtml(label)}</small><b>${escapeHtml(value)}</b></div>`; }

function initMap() {
  state.map = L.map('map', { zoomControl: false }).setView([27.2054, 88.5426], 14);
  L.control.zoom({ position: 'bottomright' }).addTo(state.map);
  const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19, attribution: 'Tiles © Esri', crossOrigin: true });
  const streets = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© OpenStreetMap' });
  const terrain = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', { maxZoom: 17, attribution: '© OpenTopoMap' });
  satellite.addTo(state.map);
  state.layers = { satellite, streets, terrain, aoi: L.featureGroup().addTo(state.map), detections: L.featureGroup().addTo(state.map), permits: L.featureGroup().addTo(state.map), protected: L.featureGroup().addTo(state.map), routes: L.featureGroup().addTo(state.map) };
  satellite.on('tileerror', () => { if (!state.map.hasLayer(streets)) { streets.addTo(state.map); notify('Satellite tiles are unavailable. Streets have been enabled as an offline-safe fallback.', 'error'); } });
  L.control.layers({ Satellite: satellite, Streets: streets, Terrain: terrain }, { 'AOI': state.layers.aoi, 'Mining / change polygons': state.layers.detections, 'Legal permit boundaries': state.layers.permits, 'Protected / sensitive zones': state.layers.protected, 'Truck routes': state.layers.routes }, { position: 'topright', collapsed: true }).addTo(state.map);
  if (L.Control.Draw) {
    state.map.addControl(new L.Control.Draw({ position: 'topright', edit: { featureGroup: state.layers.aoi }, draw: { polyline: false, circle: false, circlemarker: false, marker: false, polygon: { allowIntersection: false, shapeOptions: { color: '#71d6ff', weight: 2 } }, rectangle: { shapeOptions: { color: '#71d6ff', weight: 2 } } } }));
    state.map.on(L.Draw.Event.CREATED, event => saveDrawnAoi(event.layer));
  } else {
    notify('Map drawing tools could not be loaded. You can still use the bundled sample AOI.', 'error');
  }
}

function updateAoiReadout(aoi, area = null, center = null) {
  const geometry = aoi?.geometry || aoi;
  if (!geometry?.coordinates) return;
  const ring = geometry.coordinates[0];
  const calculatedCenter = center || { longitude: ring.reduce((sum, point) => sum + point[0], 0) / ring.length, latitude: ring.reduce((sum, point) => sum + point[1], 0) / ring.length };
  $('#aoiArea').textContent = area ? `${Number(area).toFixed(2)} ha` : '—';
  $('#aoiCenter').textContent = `${calculatedCenter.latitude.toFixed(4)}, ${calculatedCenter.longitude.toFixed(4)}`;
}
function renderAoi(aoi, area, center) {
  state.aoi = aoi;
  state.layers.aoi.clearLayers();
  const layer = L.geoJSON(aoi, { style: { color: '#71d6ff', weight: 2, fillColor: '#207a9f', fillOpacity: .08 } }).bindPopup(`<b>Area of interest</b><br>${area ? `${Number(area).toFixed(2)} ha` : 'Local AOI'}`);
  state.layers.aoi.addLayer(layer);
  updateAoiReadout(aoi, area, center);
}
async function saveDrawnAoi(layer) {
  const feature = layer.toGeoJSON();
  try {
    const saved = await api('/api/aoi', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: 'User-drawn AOI', feature }) });
    renderAoi(saved.feature, saved.area_ha, saved.center);
    state.map.fitBounds(layer.getBounds(), { padding: [25, 25] });
    notify(`AOI saved locally: ${saved.area_ha.toFixed(2)} ha. Run the selected ${$('#period').value}-day analysis.`, 'success');
  } catch (error) { notify(error.message, 'error'); }
}
function fitAoi() { const bounds = state.layers.aoi.getBounds(); if (bounds.isValid()) state.map.fitBounds(bounds, { padding: [35, 35] }); }

async function loadReferenceLayers() {
  const [permits, protectedAreas] = await Promise.all([api('/api/permits'), api('/api/protected-areas')]);
  state.layers.permits.clearLayers(); state.layers.protected.clearLayers();
  L.geoJSON(permits, { style: { color: '#60d07d', weight: 2, fillOpacity: .04 }, onEachFeature: (feature, layer) => layer.bindPopup(`<b>${escapeHtml(feature.properties.permit_id)}</b><br>Demo boundary — not official`) }).addTo(state.layers.permits);
  L.geoJSON(protectedAreas, { style: { color: '#c37eea', weight: 2, dashArray: '5 4', fillOpacity: .05 }, onEachFeature: (feature, layer) => layer.bindPopup(`<b>${escapeHtml(feature.properties.name)}</b><br>Demo boundary — not official`) }).addTo(state.layers.protected);
}

async function searchLocation(event) {
  event?.preventDefault();
  const query = $('#locationSearch').value.trim();
  if (!query) return;
  notify('Searching location…');
  try {
    const place = await api(`/api/geocode?q=${encodeURIComponent(query)}`);
    state.map.setView([place.latitude, place.longitude], place.zoom || 13);
    if (state.layers.search) state.layers.search.clearLayers(); else state.layers.search = L.featureGroup().addTo(state.map);
    L.marker([place.latitude, place.longitude]).bindPopup(`<b>${escapeHtml(place.label)}</b><br><small>${escapeHtml(place.source)}</small>`).addTo(state.layers.search).openPopup();
    notify(`Map moved to ${place.label}. ${place.data_status === 'DEMO LOCATION' ? 'This is the bundled demo location.' : 'Location found.'}`, 'success');
  } catch (error) { notify(error.message, 'error'); }
}

function modeSwitch(mode) {
  state.mode = mode;
  const data = mode === 'data';
  $('#demoMode').classList.toggle('active', !data); $('#dataMode').classList.toggle('active', data);
  $('#modeBadge').textContent = data ? '● DATA MODE' : '● DEMO DATA'; $('#modeBadge').classList.toggle('data', data);
  $('#satelliteLabel').textContent = data ? 'DATA MODE' : 'DEMO'; $('#mapStatus').textContent = `Satellite base layer · ${data ? 'DATA MODE' : 'DEMO DATA'}`;
  notify(data ? 'Data Mode uses the public Sentinel-2 catalogue and never substitutes demo detections. It needs network access and raster assets for ML polygons.' : 'Demo Mode runs entirely offline using bundled, clearly labelled fixtures.');
}

function updatePipeline(items = [], progress = 'READY') {
  $('#processPercent').textContent = progress;
  const all = ['Cloud filtering', 'AOI clip and band features', 'Mining probability mask', 'Connected polygons and permit screening'];
  $('#pipeline').innerHTML = all.map((item, index) => `<li class="${items.length > index ? 'done' : ''}">${items[index] || item}</li>`).join('');
}
function renderKpis(result) {
  const features = result.detections?.features || [];
  const props = features.map(feature => feature.properties);
  const highest = props.reduce((best, item) => !best || item.risk > best.risk ? item : best, null);
  $('#kpis').innerHTML = [kpi('Monitoring area', `${Number(result.aoi_area_ha || 0).toFixed(1)} ha`, 'blue'), kpi('Usable scenes', result.observations?.length || 0, 'lime'), kpi('Detection polygons', props.length, 'blue'), kpi('High risk', props.filter(item => ['HIGH', 'CRITICAL'].includes(item.risk_level)).length, 'red'), kpi('Mining growth', result.change ? `+${result.change.change_percentage}%` : '—', 'lime'), kpi('Affected area', `${props.reduce((sum, item) => sum + item.area_ha, 0).toFixed(1)} ha`, 'blue'), kpi('Final risk', highest ? `${highest.risk}/100` : '—', highest?.risk_level === 'CRITICAL' ? 'red' : 'lime')].join('');
}
function renderDetectionLayer(features) {
  state.layers.detections.clearLayers(); state.detections = features;
  const color = level => level === 'CRITICAL' ? '#f04f47' : level === 'HIGH' ? '#ffab39' : '#55bfe5';
  L.geoJSON({ type: 'FeatureCollection', features }, { style: feature => ({ color: color(feature.properties.risk_level), weight: 2.5, fillColor: color(feature.properties.risk_level), fillOpacity: .27 }), onEachFeature: (feature, layer) => { const item = feature.properties; layer.bindPopup(`<b>${escapeHtml(item.id)}</b><br>${escapeHtml(item.name)}<br><b>${item.probability * 100}%</b> mining-related change probability<br>Risk ${item.risk}/100 · ${escapeHtml(item.legal.classification)}`); layer.on('click', () => openCase(item.case_id)); } }).addTo(state.layers.detections);
}
function renderChange(change) {
  if (!change) { $('#changeDetails').innerHTML = '<p>No change result is available in this mode.</p>'; return; }
  $('#earliestObservation').textContent = `${formatDate(change.earliest_date)} · ${change.earliest_footprint_ha} ha`;
  $('#latestObservation').textContent = `${formatDate(change.latest_date)} · ${change.latest_footprint_ha} ha`;
  $('#changeDetails').innerHTML = `<div class="metric"><span>Mining footprint</span><b>${change.earliest_footprint_ha} → ${change.latest_footprint_ha} ha</b></div><div class="metric"><span>Increase</span><b>+${change.increase_ha} ha</b></div><div class="metric"><span>Change</span><b>+${change.change_percentage}%</b></div><div class="metric"><span>Interpretation</span><b>Requires verification</b></div>`;
}
function renderRisk(features) {
  const item = features.map(feature => feature.properties).sort((a, b) => b.risk - a.risk)[0];
  $('#openCase').disabled = !item;
  if (!item) { $('#riskScore').textContent = '—'; $('#riskLevel').textContent = 'No model result'; $('#riskBreakdown').innerHTML = ''; return; }
  $('#riskScore').textContent = `${item.risk}/100`; $('#riskLevel').textContent = `${item.risk_level} RISK · evidence support`;
  $('#riskBreakdown').innerHTML = Object.entries(item.risk_breakdown).filter(([, value]) => value > 0).map(([label, value]) => `<div class="risk-row"><span>${escapeHtml(label)}</span><b>+${value}</b></div>`).join('');
  $('#openCase').dataset.case = item.case_id;
}
function renderTimeline(observations) {
  state.observations = observations || [];
  const slider = $('#timeline'); slider.max = Math.max(0, state.observations.length - 1); slider.value = 0; slider.disabled = !state.observations.length;
  $('#timelineDates').innerHTML = state.observations.map((item, index) => `<span class="${index === 0 ? 'current' : ''}">${formatDate(item.date).replace(/ 2026/, '')}</span>`).join('');
  updateTimeline();
}
function updateTimeline() {
  const index = Number($('#timeline').value); const selected = state.observations[index];
  [...document.querySelectorAll('#timelineDates span')].forEach((item, itemIndex) => item.classList.toggle('current', itemIndex === index));
  if (!selected) { $('#selectedObservation').textContent = 'No usable observation selected.'; return; }
  $('#selectedObservation').textContent = `${formatDate(selected.date)} · ${selected.source} · ${selected.cloud_percentage}% cloud · ${selected.id}`;
  state.layers.detections.eachLayer(layer => { const date = layer.feature?.properties?.date; layer.setStyle({ fillOpacity: date && date <= selected.date ? .32 : .06, opacity: date && date <= selected.date ? 1 : .28 }); });
}
function renderTrend(observations) {
  const target = $('#trendChart');
  const usable = observations.filter(item => item.footprint_ha != null);
  if (!usable.length) { target.innerHTML = '<p>No local footprint trend is available for this Data Mode result.</p>'; return; }
  const max = Math.max(...usable.map(item => item.footprint_ha));
  target.innerHTML = usable.map(item => `<div class="trend-bar" style="height:${Math.max(16, item.footprint_ha / max * 188)}px"><b>${item.footprint_ha}</b><span>${formatDate(item.date).replace(/ 2026/, '')}</span></div>`).join('');
}
async function runAnalysis() {
  const button = $('#analyze'); button.disabled = true; button.textContent = 'Processing…'; notify(`${state.mode === 'data' ? 'Searching the public Sentinel-2 catalogue' : 'Processing bundled observations'}: filtering clouds and clipping AOI…`); updatePipeline(['Cloud filtering'], '25%');
  try {
    const result = await api('/api/satellite/analyze', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mode: state.mode, aoi: state.aoi, period_days: Number($('#period').value), cloud_max: Number($('#cloudMax').value) }) });
    state.analysis = result; renderAoi(result.aoi, result.aoi_area_ha); renderKpis(result); renderDetectionLayer(result.detections?.features || []); renderChange(result.change); renderRisk(result.detections?.features || []); renderTimeline(result.observations || []); renderTrend(result.observations || []); updatePipeline(result.pipeline || [], '100%');
    $('#periodLabel').textContent = `${$('#period').value}-day monitoring`;
    notify(result.message || 'Analysis completed.', result.mode === 'demo' ? 'success' : result.available ? 'success' : 'error');
  } catch (error) { notify(error.message, 'error'); updatePipeline([], 'ERROR'); }
  finally { button.disabled = false; button.textContent = 'Run analysis'; }
}

function compare() { if (!state.analysis?.change) { notify('Run an analysis before comparing observations.', 'error'); return; } $('#changeMode').textContent = 'COMPARE 90 DAYS ACTIVE'; $('#toggleCompare').textContent = '✓ Comparing earliest vs latest'; notify(`Compared ${formatDate(state.analysis.change.earliest_date)} and ${formatDate(state.analysis.change.latest_date)}. Change polygons remain visible on the map.`, 'success'); }
async function loadCases() {
  const result = await api('/api/cases');
  $('#caseRows').innerHTML = result.items.map(item => `<tr data-case="${escapeHtml(item.case_id)}"><td>${escapeHtml(item.case_id)}</td><td>${escapeHtml(item.location)}</td><td>${item.area_ha} ha</td><td>${Math.round(item.probability * 100)}%</td><td>+${item.change_percentage}%</td><td><span class="status-compact" title="${escapeHtml(item.legal_status)}">${escapeHtml(item.legal_status)}</span></td><td><span class="risk-pill ${item.risk_level}">${item.risk}</span></td><td><button class="case-open">Open</button></td></tr>`).join('');
}
async function loadAlerts() {
  const result = await api('/api/alerts'); $('#alertBadge').textContent = result.items.length;
  $('#alerts').innerHTML = result.items.map(item => `<div class="alert ${item.level}"><b>${escapeHtml(item.level)} · ${escapeHtml(item.type)}</b>${escapeHtml(item.message)}<br><button class="case-open" data-alert-case="${escapeHtml(item.case_id)}">Open case</button></div>`).join('');
}
async function openCase(caseId) {
  if (!caseId) return;
  try {
    const item = await api(`/api/cases/${encodeURIComponent(caseId)}`); const risk = item.risk; const detection = item.detection.properties;
    $('#caseContent').innerHTML = `<span class="eyebrow">${escapeHtml(item.data_status.satellite)} SATELLITE EVIDENCE</span><h2>${escapeHtml(item.case_id)}</h2><div class="case-summary"><b>${risk.score}/100 · ${escapeHtml(risk.level)} RISK</b><br>${escapeHtml(item.status)}</div><h3>Detection and legality screen</h3><p><b>${escapeHtml(detection.name)}</b> · ${detection.area_ha} ha · ${Math.round(detection.probability * 100)}% mining-related change probability</p><p>${escapeHtml(item.legal.classification)}<br>Inside permit: ${item.legal.inside_permit_ha} ha · Outside: ${item.legal.outside_permit_ha} ha (${item.legal.outside_percentage}%)</p><h3>Evidence fusion</h3><ul class="evidence-list">${Object.entries(risk.breakdown).filter(([, value]) => value > 0).map(([label, value]) => `<li>${escapeHtml(label)}: +${value}</li>`).join('')}</ul><h3>Next action</h3><p>Prioritise field verification. This prototype’s AI score does not prove illegal activity or legal liability.</p><p><button class="full-action" id="caseReport">Generate PDF evidence report</button></p>`;
    $('#caseDialog').showModal(); $('#caseReport').onclick = () => downloadReport(item.case_id);
  } catch (error) { notify(error.message, 'error'); }
}
async function downloadReport(caseId = 'KN-2026-001') {
  try {
    notify('Generating evidence-support PDF…');
    const response = await fetch('/api/reports/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ case_id: caseId }) });
    if (!response.ok) throw new Error('Report generation failed.');
    const blob = await response.blob(); const url = URL.createObjectURL(blob); const link = document.createElement('a'); link.href = url; link.download = `${caseId}-evidence-report.pdf`; link.click(); URL.revokeObjectURL(url); notify('PDF evidence report generated.', 'success');
  } catch (error) { notify(error.message, 'error'); }
}

function openDrone() {
  $('#droneDialog').showModal(); api('/api/drone/KN-2026-001').then(survey => {
    $('#droneMetrics').innerHTML = `<span class="eyebrow">${escapeHtml(survey.mode)}</span><span class="big">${survey.estimated_volume_m3.toLocaleString()} m³</span><div class="measure"><span>Surface area</span><b>${survey.surface_area_ha} ha</b></div><div class="measure"><span>Maximum depth</span><b>${survey.maximum_depth_m} m</b></div><div class="measure"><span>Average depth</span><b>${survey.average_depth_m} m</b></div><div class="measure"><span>Permit volume</span><b>${survey.permit_volume_m3.toLocaleString()} m³</b></div><div class="measure"><span>Difference</span><b>${survey.difference_m3.toLocaleString()} m³</b></div><p>${escapeHtml(survey.status)}</p>`; initThreeViewer();
  }).catch(error => { $('#droneMetrics').textContent = error.message; });
}
function initThreeViewer() {
  const target = $('#droneViewer'); if (!window.THREE) { target.innerHTML = '<div class="viewer-placeholder">3D viewer could not load. The sample survey measurements remain available.</div>'; return; }
  cancelAnimationFrame(state.threeFrame); if (state.threeRenderer) state.threeRenderer.dispose(); target.innerHTML = '';
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x071219); const camera = new THREE.PerspectiveCamera(42, target.clientWidth / target.clientHeight, .1, 100); camera.position.set(10, 8, 12); camera.lookAt(0, 0, 0);
  const renderer = new THREE.WebGLRenderer({ antialias: true }); renderer.setSize(target.clientWidth, target.clientHeight); renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); target.appendChild(renderer.domElement); state.threeRenderer = renderer;
  scene.add(new THREE.HemisphereLight(0xb6e6ff, 0x152a1d, 2)); const light = new THREE.DirectionalLight(0xffffff, 2); light.position.set(4, 9, 5); scene.add(light);
  const terrain = new THREE.Mesh(new THREE.PlaneGeometry(15, 12, 18, 18), new THREE.MeshStandardMaterial({ color: 0x49633d, wireframe: false, roughness: .95 })); terrain.rotation.x = -Math.PI / 2; scene.add(terrain);
  const pit = new THREE.Mesh(new THREE.ConeGeometry(3.3, 3.5, 36, 5, true), new THREE.MeshStandardMaterial({ color: 0x835a38, roughness: .8, side: THREE.DoubleSide })); pit.position.y = -.8; pit.rotation.x = Math.PI; scene.add(pit);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(3.28, .13, 10, 36), new THREE.MeshStandardMaterial({ color: 0xd3a460 })); rim.rotation.x = Math.PI / 2; rim.position.y = .03; scene.add(rim);
  const grid = new THREE.GridHelper(15, 15, 0x67935f, 0x314a32); grid.position.y = .04; scene.add(grid);
  const animate = () => { pit.rotation.z += .004; renderer.render(scene, camera); state.threeFrame = requestAnimationFrame(animate); }; animate();
}
async function openTruck() {
  $('#truckDialog').showModal();
  try {
    const route = await api('/api/trucks/TRK-SK-1042/route');
    $('#truckDetails').innerHTML = `<h3>${escapeHtml(route.vehicle_number)} · ${escapeHtml(route.status)}</h3><div class="measure"><span>Planned</span><b>${route.planned_distance_km} km</b></div><div class="measure"><span>Actual</span><b>${route.actual_distance_km} km</b></div><div class="measure"><span>Deviation</span><b>+${route.distance_difference_km} km (${route.route_deviation_percentage}%)</b></div><div class="measure"><span>Unexpected stop</span><b>${route.unexpected_stop_min} min</b></div><div class="measure"><span>Missing checkpoint</span><b>${route.missing_checkpoints}</b></div><p>GPS is simulated. RFID, e-Challan and weighbridge evidence is included in case KN-2026-001.</p>`;
    renderTruckMap(route);
  } catch (error) { $('#truckDetails').textContent = error.message; }
}
function renderTruckMap(route) {
  if (state.truckMap) { state.truckMap.remove(); state.truckMap = null; }
  state.truckMap = L.map('truckMap', { zoomControl: false, attributionControl: false });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(state.truckMap);
  const planned = route.planned.map(point => [point[1], point[0]]); const actual = route.actual.map(point => [point[1], point[0]]);
  L.polyline(planned, { color: '#6bdb85', weight: 4, dashArray: '6 5' }).bindPopup('Planned route').addTo(state.truckMap); L.polyline(actual, { color: '#ffbd42', weight: 4 }).bindPopup('Actual route').addTo(state.truckMap);
  route.checkpoints.forEach(item => L.circleMarker([item.coordinates[1], item.coordinates[0]], { radius: 6, color: item.seen ? '#66db82' : '#ef5b50', fillOpacity: 1 }).bindPopup(`${item.name}: ${item.seen ? 'RFID seen' : 'checkpoint missing'}`).addTo(state.truckMap));
  L.marker(actual.at(-1)).bindPopup('Destination').addTo(state.truckMap); state.truckMap.fitBounds(L.featureGroup([L.polyline(planned), L.polyline(actual)]).getBounds(), { padding: [20, 20] }); setTimeout(() => state.truckMap.invalidateSize(), 80);
}
async function uploadDrone(event) {
  event.preventDefault(); const file = $('#droneFile').files[0]; if (!file) { $('#uploadStatus').textContent = 'Choose a permitted image first.'; return; }
  $('#uploadStatus').textContent = 'Storing…';
  try { const result = await api(`/api/drone/upload?case_id=KN-2026-001&filename=${encodeURIComponent(file.name)}`, { method: 'POST', headers: { 'Content-Type': file.type || 'application/octet-stream' }, body: file }); $('#uploadStatus').textContent = result.message; } catch (error) { $('#uploadStatus').textContent = error.message; }
}
function playTimeline() { if (!state.observations.length) return; clearInterval(state.timelineTimer); state.timelineTimer = setInterval(() => { const slider = $('#timeline'); slider.value = Number(slider.value) >= Number(slider.max) ? 0 : Number(slider.value) + 1; updateTimeline(); }, 900); }
function pauseTimeline() { clearInterval(state.timelineTimer); state.timelineTimer = null; }

async function initialise() {
  setClock(); setInterval(setClock, 30000); initMap();
  try {
    state.config = await api('/api/config'); const storedAoi = await api('/api/aoi'); renderAoi(storedAoi.feature, storedAoi.area_ha, storedAoi.center); state.map.setView([state.config.demo_location.latitude, state.config.demo_location.longitude], state.config.demo_location.zoom);
    await Promise.all([loadReferenceLayers(), loadCases(), loadAlerts()]); await runAnalysis();
  } catch (error) { notify(`The workspace could not initialise: ${error.message}`, 'error'); }
}

$('#searchForm').addEventListener('submit', searchLocation); $('#demoMode').onclick = () => modeSwitch('demo'); $('#dataMode').onclick = () => modeSwitch('data'); $('#sampleAoi').onclick = () => { const sample = state.config.sample_aoi; renderAoi(sample, null); fitAoi(); notify('Sample AOI loaded. This local polygon is clearly labelled DEMO DATA.', 'success'); }; $('#analyze').onclick = runAnalysis; $('#fitAoi').onclick = fitAoi; $('#toggleCompare').onclick = compare; $('#timeline').oninput = updateTimeline; $('#playTimeline').onclick = playTimeline; $('#pauseTimeline').onclick = pauseTimeline; $('#openCase').onclick = () => openCase($('#openCase').dataset.case); $('#droneUpload').addEventListener('submit', uploadDrone);
document.addEventListener('click', event => { const close = event.target.closest('[data-close]'); if (close) $(`#${close.dataset.close}`).close(); const dialog = event.target.closest('[data-dialog]'); if (dialog) { if (dialog.dataset.dialog === 'droneDialog') openDrone(); else if (dialog.dataset.dialog === 'truckDialog') openTruck(); } const caseRow = event.target.closest('[data-case]'); if (caseRow) openCase(caseRow.dataset.case); const alertCase = event.target.closest('[data-alert-case]'); if (alertCase) openCase(alertCase.dataset.alertCase); const scroll = event.target.closest('[data-scroll]'); if (scroll) $(`#${scroll.dataset.scroll}`).scrollIntoView({ behavior: 'smooth' }); });
window.addEventListener('resize', () => { state.map?.invalidateSize(); if (state.truckMap) state.truckMap.invalidateSize(); }); initialise();
