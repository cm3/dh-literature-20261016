(function () {
  "use strict";

  const refs = Array.from(document.querySelectorAll(".note-ref"));
  const panel = document.getElementById("reading-note-panel");
  const progress = document.querySelector(".reading-progress span");
  const placeholder = panel.querySelector(".note-placeholder")?.cloneNode(true);
  const catalog = new Map(
    Array.from(document.querySelectorAll(".note-catalog .note-entry")).map((entry) => [
      entry.dataset.noteId,
      entry,
    ])
  );
  let activeId = null;
  let manualId = null;

  function setActive(id) {
    if (!id || !catalog.has(id) || activeId === id) return;
    activeId = id;
    document.querySelectorAll(".annotated-term.is-active").forEach((term) => {
      term.classList.remove("is-active");
    });
    document
      .querySelector(`[data-note-anchor="${CSS.escape(id)}"]`)
      ?.classList.add("is-active");

    const clone = catalog.get(id).cloneNode(true);
    clone.removeAttribute("id");
    clone.querySelector(".note-back")?.remove();
    panel.replaceChildren(clone);
  }

  function clearActive() {
    if (!activeId) return;
    activeId = null;
    document.querySelectorAll(".annotated-term.is-active").forEach((term) => {
      term.classList.remove("is-active");
    });
    if (placeholder) panel.replaceChildren(placeholder.cloneNode(true));
    else panel.replaceChildren();
  }

  function nearestReadingNote() {
    if (manualId) return manualId;
    const height = window.innerHeight || document.documentElement.clientHeight;
    const upper = height * 0.11;
    const lower = height * 0.78;
    const focus = height * 0.36;
    const candidates = refs
      .map((ref) => ({ ref, rect: ref.getBoundingClientRect() }))
      .filter(({ rect }) => rect.bottom >= upper && rect.top <= lower)
      .sort(
        (a, b) =>
          Math.abs((a.rect.top + a.rect.bottom) / 2 - focus) -
          Math.abs((b.rect.top + b.rect.bottom) / 2 - focus)
      );
    return candidates[0]?.ref.dataset.noteId || null;
  }

  function update() {
    const id = nearestReadingNote();
    if (id) setActive(id);
    else clearActive();

    const root = document.documentElement;
    const maximum = root.scrollHeight - root.clientHeight;
    const ratio = maximum > 0 ? window.scrollY / maximum : 0;
    progress.style.transform = `scaleX(${Math.min(1, Math.max(0, ratio))})`;
  }

  function requestUpdate() {
    update();
  }

  refs.forEach((ref) => {
    ref.addEventListener("click", () => {
      manualId = ref.dataset.noteId;
      setActive(manualId);
    });
    ref.addEventListener("focus", () => {
      manualId = ref.dataset.noteId;
      setActive(manualId);
    });
    ref.addEventListener("blur", (event) => {
      if (event.relatedTarget?.closest("#reading-note-panel")) return;
      manualId = null;
      requestUpdate();
    });
  });

  document.querySelectorAll(".chapter-nav button").forEach((button) => {
    if (!button.dataset.chapter) return;
    button.addEventListener("click", () => {
      const heading = Array.from(document.querySelectorAll(".reading-text > h1")).find(
        (candidate) => candidate.textContent.includes(button.dataset.chapter)
      );
      heading?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  function onScroll() {
    manualId = null;
    requestUpdate();
  }

  document.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", requestUpdate);
  window.addEventListener("load", requestUpdate);
  requestUpdate();

  const mapDialog = document.getElementById("place-map-dialog");
  const openMap = document.getElementById("open-place-map");
  const closeMap = document.getElementById("close-place-map");
  const mapElement = document.getElementById("place-map");
  const mapStatus = document.getElementById("map-status");
  const mapStatusTitle = document.getElementById("map-status-title");
  const mapStatusDetail = document.getElementById("map-status-detail");
  const mapHttpLink = document.getElementById("map-http-link");
  const mapRetry = document.getElementById("map-retry");
  const places = JSON.parse(document.getElementById("place-data")?.textContent || "[]");
  let map = null;
  let markerLayer = null;
  let tiles = null;
  let tileErrors = 0;
  let tileTimer = null;
  const placeMarkers = new Map();

  function showMapStatus(title, detail, { httpLink = false, retry = false } = {}) {
    mapStatusTitle.textContent = title;
    mapStatusDetail.textContent = detail;
    mapHttpLink.hidden = !httpLink;
    mapRetry.hidden = !retry;
    mapStatus.hidden = false;
  }

  function checkMapConnection() {
    if (!navigator.onLine) {
      clearTimeout(tileTimer);
      if (map && tiles && map.hasLayer(tiles)) map.removeLayer(tiles);
      showMapStatus("オフラインのため、地図を利用できません", "インターネットに接続してから地図を開き直してください。地名一覧と解説は、このまま読めます。");
      return false;
    }
    if (location.protocol === "file:") {
      showMapStatus("地図はローカルサーバー経由で開いてください", "ファイルを直接開くと、背景地図の配信元に拒否されることがあります。ローカルサーバーを起動して、下のリンクから開いてください。", { httpLink: true });
      return false;
    }
    return true;
  }

  function markerIcon(kind) {
    return L.divIcon({
      className: "place-marker-wrap",
      html: `<span class="place-marker place-marker-${kind}"></span>`,
      iconSize: [18, 18],
      iconAnchor: [9, 9],
      popupAnchor: [0, -10],
    });
  }

  function popupFor(place) {
    const popup = document.createElement("div");
    popup.className = "map-popup";
    const title = document.createElement("h3");
    title.textContent = place.name;
    const status = document.createElement("p");
    status.className = "map-popup-status";
    status.textContent = place.status;
    const detail = document.createElement("p");
    detail.textContent = place.detail;
    const links = document.createElement("p");
    links.className = "map-popup-links";
    const osm = document.createElement("a");
    osm.href = `https://www.openstreetmap.org/?mlat=${place.lat}&mlon=${place.lon}#map=14/${place.lat}/${place.lon}`;
    osm.target = "_blank";
    osm.rel = "noreferrer";
    osm.textContent = "OpenStreetMap";
    links.appendChild(osm);
    if (place.source_url) {
      links.append(" · ");
      const source = document.createElement("a");
      source.href = place.source_url;
      source.target = "_blank";
      source.rel = "noreferrer";
      source.textContent = "典拠";
      links.appendChild(source);
    }
    popup.append(title, status, detail, links);
    const photos = document.querySelectorAll(`.place-entry[data-place-id="${place.id}"] .place-photo`);
    photos.forEach((photo) => {
      const figure = photo.cloneNode(true);
      figure.querySelector("img").loading = "eager";
      popup.appendChild(figure);
    });
    return popup;
  }

  function initMap() {
    if (!mapElement || !checkMapConnection()) return;
    if (map) {
      if (!map.hasLayer(tiles)) {
        mapStatus.hidden = true;
        tiles.addTo(map);
      }
      return;
    }
    if (!window.L) {
      showMapStatus("地図を読み込めませんでした", "インターネット接続を確認し、ページを再読み込みしてください。地名一覧と解説は、このまま読めます。", { retry: true });
      return;
    }
    mapStatus.hidden = true;
    map = L.map(mapElement, { scrollWheelZoom: true });
    tiles = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      referrerPolicy: "strict-origin-when-cross-origin",
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
    });
    const tileFailure = () => {
      if (!checkMapConnection()) return;
      showMapStatus("背景地図を読み込めませんでした", "接続不良、または地図配信元の制限が考えられます。接続を確認し、少し待ってから再読み込みしてください。地名一覧と解説は読めます。", { retry: true });
    };
    tiles.on("loading", () => {
      tileErrors = 0;
      clearTimeout(tileTimer);
      tileTimer = setTimeout(tileFailure, 15000);
    });
    tiles.on("tileerror", () => {
      tileErrors += 1;
      clearTimeout(tileTimer);
      tileFailure();
    });
    tiles.on("load", () => {
      clearTimeout(tileTimer);
      if (tileErrors === 0 && checkMapConnection()) mapStatus.hidden = true;
    });
    tiles.addTo(map);
    markerLayer = L.layerGroup().addTo(map);
    places.forEach((place) => {
      if (place.lat === null || place.lon === null) return;
      const marker = L.marker([place.lat, place.lon], {
        icon: markerIcon(place.kind),
        title: place.name,
      }).bindPopup(popupFor(place), { maxWidth: 300, maxHeight: 420 });
      marker.on("click", () => highlightPlace(place.id));
      placeMarkers.set(place.id, { marker, place });
    });
    showMapView("thames");
  }

  function placesForView(view) {
    return places.filter((place) => {
      if (place.lat === null || place.lon === null) return false;
      if (view === "thames") return place.region === "thames";
      if (view === "uk") return place.region !== "world";
      return true;
    });
  }

  function showMapView(view) {
    if (!map || !markerLayer) return;
    markerLayer.clearLayers();
    const visible = placesForView(view);
    visible.forEach((place) => markerLayer.addLayer(placeMarkers.get(place.id).marker));
    const bounds = L.latLngBounds(visible.map((place) => [place.lat, place.lon]));
    map.fitBounds(bounds, {
      padding: [28, 28],
      maxZoom: view === "thames" ? 11 : 6,
    });
    document.querySelectorAll("[data-map-view]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.mapView === view));
    });
  }

  function highlightPlace(placeId) {
    let selected = null;
    document.querySelectorAll(".place-list .place-entry[data-place-id]").forEach((entry) => {
      const matches = entry.dataset.placeId === placeId;
      entry.classList.toggle("is-selected", matches);
      if (matches) {
        entry.setAttribute("aria-current", "location");
        selected = entry;
      } else entry.removeAttribute("aria-current");
    });
    if (selected) {
      const list = document.querySelector(".place-list");
      list.scrollTo({ top: list.scrollTop + selected.getBoundingClientRect().top - list.getBoundingClientRect().top - 4 });
    }
  }

  function focusPlace(placeId) {
    highlightPlace(placeId);
    const item = placeMarkers.get(placeId);
    if (!item || !map) {
      map?.closePopup();
      return;
    }
    // Keep neighbouring reference points visible (notably the two Yorkshire
    // peaks), even when opening a UK location from the default Thames view.
    placeMarkers.forEach(({ marker }) => markerLayer.addLayer(marker));
    map.closePopup();
    map.setView([item.place.lat, item.place.lon], item.place.zoom || 13, { animate: false });
    // The selected card already shows the details. A popup here can auto-pan
    // the short map away from the requested marker.
    document.querySelectorAll("[data-map-view]").forEach((button) => button.setAttribute("aria-pressed", "false"));
  }

  function openPlaceMap(placeId = null) {
    if (!mapDialog.open) mapDialog.showModal();
    initMap();
    // showModal makes the layout measurable immediately. Do not defer the
    // requested selection to a frame that may be suspended in a background tab.
    map?.invalidateSize({ pan: false });
    if (placeId) focusPlace(placeId);
  }

  openMap?.addEventListener("click", () => openPlaceMap());
  document.addEventListener("click", (event) => {
    const link = event.target.closest("[data-show-place]");
    if (!link) return;
    event.preventDefault();
    openPlaceMap(link.dataset.showPlace);
  });
  mapRetry?.addEventListener("click", () => location.reload());
  window.addEventListener("offline", checkMapConnection);
  window.addEventListener("online", () => {
    if (mapDialog.open) initMap();
  });
  closeMap?.addEventListener("click", () => mapDialog.close());
  mapDialog?.addEventListener("click", (event) => {
    if (event.target === mapDialog) mapDialog.close();
  });
  document.querySelectorAll("[data-map-view]").forEach((button) => {
    button.addEventListener("click", () => showMapView(button.dataset.mapView));
  });
  document.querySelectorAll(".place-entry[data-place-id]").forEach((entry) => {
    const place = places.find((candidate) => candidate.id === entry.dataset.placeId);
    if (!place) return;
    entry.tabIndex = 0;
    entry.addEventListener("click", (event) => {
      if (!event.target.closest("a, button")) focusPlace(place.id);
    });
    entry.addEventListener("keydown", (event) => {
      if (event.target !== entry) return;
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        focusPlace(place.id);
      }
    });
  });
  if (location.hash === "#place-map-dialog") openPlaceMap();
})();
