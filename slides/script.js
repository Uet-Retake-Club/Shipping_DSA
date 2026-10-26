/* =====================================================================
   SHIPPING_DSA | MINIMALIST PRESENTATION ENGINE
   Controls: Navigation, Timer, Speaker Notes, Overview & Graph Visualizer
   ===================================================================== */

// Presentation State
const state = {
  currentSlide: 1,
  totalSlides: 12,
  timerSeconds: 0,
  timerInterval: null,
  timerRunning: false,
  notesVisible: false,
  overviewVisible: false
};

// Speaker Notes Data per Slide (Clean Typographic Text)
const speakerNotes = {
  1: `<strong>Slide 01: Giới thiệu dự án</strong><br><br>
  - Chào mừng Thầy/Cô và các bạn đến với buổi báo cáo đề tài Cấu trúc Dữ liệu & Giải thuật.<br>
  - Đề tài: <em>Thiết kế mạng lưới giao vận thông minh bằng Cây bao trùm nhỏ nhất (MST)</em>.<br>
  - Nhấn mạnh: Cốt lõi của đề tài là tự cài đặt các cấu trúc dữ liệu nâng cao (DSU, Min-Heap) và áp dụng vào bài toán thực tế quy hoạch mạng bưu chính tại Hà Nội.`,

  2: `<strong>Slide 02: Đặt vấn đề & Động lực nghiên cứu</strong><br><br>
  - Nêu bài toán thực tế: Các doanh nghiệp giao vận đối mặt bài toán chi phí hạ tầng hàng triệu USD.<br>
  - Phân biệt rõ: <strong>MST</strong> (quy hoạch hạ tầng kết nối cố định) khác với <strong>Dijkstra</strong> (đường đi ngắn nhất giữa 2 điểm) và <strong>TSP</strong> (lộ trình 1 xe giao hàng).<br>
  - Trọng tâm: Kết nối 100% các kho với chi phí nhỏ nhất mà không tạo kết nối dư thừa.`,

  3: `<strong>Slide 03: Mô hình hóa Đồ thị & Dữ liệu Thực tế</strong><br><br>
  - Đồ thị vô hướng <em>G = (V, E)</em>.<br>
  - 3 phân tầng điểm nút: Central Mega Hub (Kho tổng), Regional Warehouse (Kho trung chuyển), Delivery Point (Bưu cục).<br>
  - Nhấn mạnh: Tọa độ GPS thực tế được xử lý bằng công thức mặt cầu <strong>Haversine</strong> để tính độ cong Trái Đất chính xác.`,

  4: `<strong>Slide 04: Cơ sở Toán học & Tính chất Lát cắt</strong><br><br>
  - <strong>Cut Property (Tính chất lát cắt):</strong> Cạnh nhẹ nhất băng qua bất kỳ lát cắt nào chia đôi đồ thị luôn thuộc về mọi MST.<br>
  - <strong>Cycle Property (Tính chất chu trình):</strong> Cạnh nặng nhất trong chu trình không bao giờ thuộc MST.<br>
  - Đây là nền tảng toán học bảo đảm tính đúng đắn cho chiến lược Tham lam (Greedy).`,

  5: `<strong>Slide 05: Thuật toán Borůvka (1926)</strong><br><br>
  - Thuật toán MST đầu tiên trong lịch sử, ra đời trước Kruskal và Prim 3 thập kỷ để thiết kế lưới điện Moravia.<br>
  - Hoạt động: Co cụm song song từng vòng (Round). Mỗi vòng giảm ít nhất 50% số component.<br>
  - Số vòng tối đa ≤ ⌈log₂ V⌉. Rất mạnh mẽ khi chạy trên kiến trúc đa luồng hoặc phân tán.`,

  6: `<strong>Slide 06: Thuật toán Kruskal & Tối ưu hóa DSU</strong><br><br>
  - Cách tiếp cận: Duyệt các cạnh theo thứ tự trọng số tăng dần.<br>
  - <strong>Điểm ăn điểm kỹ thuật:</strong> Tự cài đặt Disjoint Set Union với <em>Path Compression</em> và <em>Union by Rank</em>.<br>
  - Thao tác tìm gốc và gộp đạt thời gian <em>O(α(V)) ≈ O(1)</em>. Tổng độ phức tạp chỉ còn <em>O(E log E)</em> cho bước sắp xếp.`,

  7: `<strong>Slide 07: Thuật toán Prim & Min-Heap Nâng cao</strong><br><br>
  - Cách tiếp cận: Nuôi lớn một cây liên thông duy nhất từ 1 đỉnh.<br>
  - Đối chiếu 2 phiên bản:<br>
    + <em>Lazy Prim:</em> Min-Heap lưu mọi cạnh kề, bộ nhớ <em>O(E)</em>.<br>
    + <em>Eager Prim:</em> Dùng IndexedMinHeap hỗ trợ <code>decrease_key</code>, chỉ lưu <em>O(V)</em> đỉnh, tốc độ <em>O(E log V)</em>.<br>
  - Cây luôn liên thông tại mọi bước, phù hợp thi công thực tế.`,

  8: `<strong>Slide 08: Ma trận So sánh Toàn diện</strong><br><br>
  - Đồ thị thưa (<em>E ≈ V</em>): Kruskal chiếm ưu thế tuyệt đối do sort ít cạnh.<br>
  - Đồ thị dày (<em>E ≈ V²</em>): Eager Prim thắng thế vì không cần sắp xếp <em>O(V²)</em> cạnh.<br>
  - Đồ thị không liên thông: Kruskal và Borůvka cho ra Rừng MST (MSF) một cách tự nhiên.`,

  9: `<strong>Slide 09: Demo Mô phỏng Tương tác</strong><br><br>
  - Hướng dẫn trực tiếp trên màn hình: Bấm nút 'Từng bước (Step)' để xem thuật toán Kruskal/Prim chọn cạnh.<br>
  - Giải thích hiện tượng loại bỏ cạnh tạo chu trình: DSU kiểm tra <code>find(u) == find(v)</code> nên cạnh bị từ chối.<br>
  - Chỉ ra tổng trọng số hội tụ về mức tối ưu toàn cục.`,

  10: `<strong>Slide 10: Case Study Mạng lưới Hà Nội</strong><br><br>
  - Dữ liệu 22 nút bưu chính tại Hà Nội (3 Hub, 9 Warehouse, 10 trạm phát).<br>
  - Kết quả: Từ 30 tuyến đường ban đầu giảm xuống đúng 21 tuyến trục (V - 1).<br>
  - Tổng chi phí giảm từ 184.2 xuống 118.6 đơn vị (Tiết kiệm 35.6% ngân sách đầu tư).`,

  11: `<strong>Slide 11: Đánh giá Rủi ro & Hướng Phát triển</strong><br><br>
  - Nêu tư duy phản biện: Nhược điểm của cây là điểm lỗi đơn lẻ (Single Point of Failure). Nếu 1 cầu trục đứt, mạng lưới bị chia rẽ.<br>
  - Giải pháp thực tế: Bổ sung các cạnh dự phòng (2-Edge Connected Network) và kết hợp với bài toán định tuyến xe VRP.`,

  12: `<strong>Slide 12: Tổng kết & Vấn đáp Phản biện (Q&A)</strong><br><br>
  - Tóm tắt 4 trụ cột đã hoàn thành.<br>
  - Mời Hội đồng / Giảng viên đặt câu hỏi.<br>
  - Bấm vào các câu hỏi mẫu để xem nhanh đáp án chuẩn bị sẵn cho buổi bảo vệ.`
};

// DOM Elements
const slides = document.querySelectorAll('.slide');
const currentSlideNumEl = document.getElementById('currentSlideNum');
const totalSlideNumEl = document.getElementById('totalSlideNum');
const progressFill = document.getElementById('progressFill');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const notesModal = document.getElementById('notesModal');
const notesBody = document.getElementById('notesBody');
const toggleNotesBtn = document.getElementById('toggleNotesBtn');
const overviewModal = document.getElementById('overviewModal');
const overviewGrid = document.getElementById('overviewGrid');
const toggleOverviewBtn = document.getElementById('toggleOverviewBtn');
const fullscreenBtn = document.getElementById('fullscreenBtn');
const timerDisplay = document.getElementById('timerDisplay');
const toggleTimerBtn = document.getElementById('toggleTimerBtn');
const resetTimerBtn = document.getElementById('resetTimerBtn');
const timerWidget = document.getElementById('timerWidget');

// Initialize Presentation
function initPresentation() {
  state.totalSlides = slides.length;
  if (totalSlideNumEl) {
    totalSlideNumEl.textContent = String(state.totalSlides).padStart(2, '0');
  }
  
  updateSlideView();
  startTimer();
  buildOverviewGrid();
  setupEventListeners();
  initSimulator();
}

// Update Slide Display
function updateSlideView() {
  slides.forEach((slide, idx) => {
    slide.classList.remove('active', 'prev', 'next');
    const slideNum = idx + 1;
    if (slideNum === state.currentSlide) {
      slide.classList.add('active');
    } else if (slideNum < state.currentSlide) {
      slide.classList.add('prev');
    } else {
      slide.classList.add('next');
    }
  });

  // Update counters & progress bar
  if (currentSlideNumEl) {
    currentSlideNumEl.textContent = String(state.currentSlide).padStart(2, '0');
  }
  if (progressFill) {
    const progressPercent = (state.currentSlide / state.totalSlides) * 100;
    progressFill.style.width = `${progressPercent}%`;
  }

  // Update speaker notes
  if (notesBody) {
    if (speakerNotes[state.currentSlide]) {
      notesBody.innerHTML = speakerNotes[state.currentSlide];
    } else {
      notesBody.innerHTML = `<em>Không có ghi chú cho slide này.</em>`;
    }
  }

  // Update overview thumbnail highlighting
  const thumbs = document.querySelectorAll('.overview-thumb');
  thumbs.forEach((thumb, idx) => {
    if (idx + 1 === state.currentSlide) {
      thumb.classList.add('current');
    } else {
      thumb.classList.remove('current');
    }
  });
}

function nextSlide() {
  if (state.currentSlide < state.totalSlides) {
    state.currentSlide++;
    updateSlideView();
  }
}

function prevSlide() {
  if (state.currentSlide > 1) {
    state.currentSlide--;
    updateSlideView();
  }
}

function goToSlide(num) {
  if (num >= 1 && num <= state.totalSlides) {
    state.currentSlide = num;
    updateSlideView();
    closeOverview();
  }
}

// Timer Functions
function startTimer() {
  if (!state.timerInterval) {
    state.timerRunning = true;
    if (toggleTimerBtn) toggleTimerBtn.textContent = '⏸';
    state.timerInterval = setInterval(() => {
      state.timerSeconds++;
      renderTimer();
    }, 1000);
  }
}

function pauseTimer() {
  if (state.timerInterval) {
    clearInterval(state.timerInterval);
    state.timerInterval = null;
    state.timerRunning = false;
    if (toggleTimerBtn) toggleTimerBtn.textContent = '▶';
  }
}

function resetTimer() {
  pauseTimer();
  state.timerSeconds = 0;
  renderTimer();
  if (timerWidget) timerWidget.classList.remove('warning', 'danger');
}

function toggleTimer() {
  if (state.timerRunning) {
    pauseTimer();
  } else {
    startTimer();
  }
}

function renderTimer() {
  if (!timerDisplay) return;
  const mins = Math.floor(state.timerSeconds / 60);
  const secs = state.timerSeconds % 60;
  timerDisplay.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

  // Time warnings (10 mins warning, 13 mins danger)
  if (timerWidget) {
    if (mins >= 13) {
      timerWidget.classList.add('danger');
      timerWidget.classList.remove('warning');
    } else if (mins >= 10) {
      timerWidget.classList.add('warning');
      timerWidget.classList.remove('danger');
    } else {
      timerWidget.classList.remove('warning', 'danger');
    }
  }
}

// Modals: Speaker Notes & Overview
function toggleNotes() {
  state.notesVisible = !state.notesVisible;
  if (notesModal && toggleNotesBtn) {
    if (state.notesVisible) {
      notesModal.classList.add('show');
      toggleNotesBtn.classList.add('active');
    } else {
      notesModal.classList.remove('show');
      toggleNotesBtn.classList.remove('active');
    }
  }
}

function openOverview() {
  state.overviewVisible = true;
  if (overviewModal && toggleOverviewBtn) {
    overviewModal.classList.add('show');
    toggleOverviewBtn.classList.add('active');
  }
}

function closeOverview() {
  state.overviewVisible = false;
  if (overviewModal && toggleOverviewBtn) {
    overviewModal.classList.remove('show');
    toggleOverviewBtn.classList.remove('active');
  }
}

function toggleOverview() {
  if (state.overviewVisible) {
    closeOverview();
  } else {
    openOverview();
  }
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(err => {
      console.log('Fullscreen error:', err);
    });
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  }
}

// Build Overview Grid Thumbnails
function buildOverviewGrid() {
  if (!overviewGrid) return;
  overviewGrid.innerHTML = '';
  slides.forEach((slide, idx) => {
    const slideNum = idx + 1;
    const titleEl = slide.querySelector('.slide-title') || slide.querySelector('.hero-heading');
    const title = titleEl ? titleEl.textContent.trim() : `Slide ${slideNum}`;

    const thumb = document.createElement('div');
    thumb.className = `overview-thumb ${slideNum === state.currentSlide ? 'current' : ''}`;
    thumb.innerHTML = `
      <div class="thumb-num">SLIDE ${String(slideNum).padStart(2, '0')}</div>
      <div class="thumb-title">${title}</div>
    `;
    thumb.addEventListener('click', () => goToSlide(slideNum));
    overviewGrid.appendChild(thumb);
  });
}

// Event Listeners (Keyboard & Controls)
function setupEventListeners() {
  if (prevBtn) prevBtn.addEventListener('click', prevSlide);
  if (nextBtn) nextBtn.addEventListener('click', nextSlide);

  if (toggleNotesBtn) toggleNotesBtn.addEventListener('click', toggleNotes);
  if (toggleOverviewBtn) toggleOverviewBtn.addEventListener('click', toggleOverview);
  if (fullscreenBtn) fullscreenBtn.addEventListener('click', toggleFullscreen);
  if (toggleTimerBtn) toggleTimerBtn.addEventListener('click', toggleTimer);
  if (resetTimerBtn) resetTimerBtn.addEventListener('click', resetTimer);

  const closeNotesBtn = document.getElementById('closeNotesBtn');
  if (closeNotesBtn) closeNotesBtn.addEventListener('click', toggleNotes);

  const closeOverviewBtn = document.getElementById('closeOverviewBtn');
  if (closeOverviewBtn) closeOverviewBtn.addEventListener('click', closeOverview);

  const progressTrack = document.getElementById('progressTrack');
  if (progressTrack) {
    progressTrack.addEventListener('click', (e) => {
      const rect = progressTrack.getBoundingClientRect();
      const clickPos = (e.clientX - rect.left) / rect.width;
      const targetSlide = Math.min(state.totalSlides, Math.max(1, Math.ceil(clickPos * state.totalSlides)));
      goToSlide(targetSlide);
    });
  }

  // Keyboard Navigation
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (state.overviewVisible) closeOverview();
      if (state.notesVisible) toggleNotes();
      return;
    }

    switch (e.key) {
      case 'ArrowRight':
      case 'PageDown':
      case ' ':
        e.preventDefault();
        nextSlide();
        break;
      case 'ArrowLeft':
      case 'PageUp':
        e.preventDefault();
        prevSlide();
        break;
      case 'Home':
        e.preventDefault();
        goToSlide(1);
        break;
      case 'End':
        e.preventDefault();
        goToSlide(state.totalSlides);
        break;
      case 's':
      case 'S':
        e.preventDefault();
        toggleNotes();
        break;
      case 'o':
      case 'O':
        e.preventDefault();
        toggleOverview();
        break;
      case 'f':
      case 'F':
        e.preventDefault();
        toggleFullscreen();
        break;
    }
  });

  // Accordion for Q&A on Slide 12
  document.querySelectorAll('.qa-card').forEach(card => {
    card.addEventListener('click', () => {
      card.classList.toggle('open');
    });
  });
}

/* =====================================================================
   INTERACTIVE ALGORITHM SIMULATOR (SLIDE 09)
   Fully Interactable Schematic: Draggable Nodes, Start-node Picking, Hover
   ===================================================================== */
const DEFAULT_SIM_NODES = [
  { id: 'H01', name: 'Long Biên Hub', x: 420, y: 90, type: 'hub' },
  { id: 'D02', name: 'Hoàn Kiếm Post', x: 300, y: 80, type: 'delivery' },
  { id: 'W02', name: 'Đống Đa DC', x: 270, y: 210, type: 'warehouse' },
  { id: 'W01', name: 'Cầu Giấy DC', x: 130, y: 120, type: 'warehouse' },
  { id: 'D01', name: 'Mỹ Đình Post', x: 80, y: 260, type: 'delivery' },
  { id: 'W03', name: 'Hà Đông DC', x: 200, y: 330, type: 'warehouse' }
];

// Working copy of nodes that can be dragged
let simNodes = JSON.parse(JSON.stringify(DEFAULT_SIM_NODES));

const simEdges = [
  { u: 'W01', v: 'D01', w: 4.8 },
  { u: 'D02', v: 'W02', w: 5.5 },
  { u: 'H01', v: 'D02', w: 6.0 },
  { u: 'W01', v: 'W02', w: 7.2 },
  { u: 'W02', v: 'W03', w: 9.1 },
  { u: 'W03', v: 'D01', w: 12.0 },
  { u: 'H01', v: 'W02', w: 14.5 }
];

let simState = {
  algo: 'kruskal',
  primStartNode: 'H01',
  stepIndex: 0,
  mstEdges: [],
  totalWeight: 0,
  dsuParent: {},
  visitedPrim: new Set(['H01']),
  autoInterval: null,
  sortedEdges: [],
  hoveredNode: null,
  hoveredEdge: null
};

// Drag State
let dragInfo = {
  node: null,
  offsetX: 0,
  offsetY: 0
};

function initSimulator() {
  simState.sortedEdges = [...simEdges].sort((a, b) => a.w - b.w);
  resetSimState();

  const kruskalBtn = document.getElementById('simKruskalBtn');
  const primBtn = document.getElementById('simPrimBtn');
  const stepBtn = document.getElementById('simStepBtn');
  const autoBtn = document.getElementById('simAutoBtn');
  const resetBtn = document.getElementById('simResetBtn');
  const resetLayoutBtn = document.getElementById('resetLayoutBtn');

  if (kruskalBtn) {
    kruskalBtn.addEventListener('click', () => {
      setSimAlgo('kruskal');
      kruskalBtn.classList.add('active-algo');
      if (primBtn) primBtn.classList.remove('active-algo');
    });
  }

  if (primBtn) {
    primBtn.addEventListener('click', () => {
      setSimAlgo('prim');
      primBtn.classList.add('active-algo');
      if (kruskalBtn) kruskalBtn.classList.remove('active-algo');
    });
  }

  if (stepBtn) stepBtn.addEventListener('click', runSimStep);
  if (autoBtn) autoBtn.addEventListener('click', toggleSimAuto);
  if (resetBtn) resetBtn.addEventListener('click', resetSimState);

  if (resetLayoutBtn) {
    resetLayoutBtn.addEventListener('click', () => {
      simNodes = JSON.parse(JSON.stringify(DEFAULT_SIM_NODES));
      renderGraph();
      setCanvasStatus('Đã khôi phục bố cục đỉnh mặc định.');
    });
  }

  setupCanvasDragging();
  renderGraph();
}

function setSimAlgo(algo) {
  simState.algo = algo;
  resetSimState();
}

function resetSimState() {
  if (simState.autoInterval) {
    clearInterval(simState.autoInterval);
    simState.autoInterval = null;
    const autoBtn = document.getElementById('simAutoBtn');
    if (autoBtn) autoBtn.textContent = 'Tự động';
  }

  simState.stepIndex = 0;
  simState.mstEdges = [];
  simState.totalWeight = 0;
  simState.visitedPrim = new Set([simState.primStartNode]);

  simState.dsuParent = {};
  simNodes.forEach(n => simState.dsuParent[n.id] = n.id);

  updateSimStats();
  clearSimLog();

  if (simState.algo === 'kruskal') {
    addSimLog('Thuật toán: KRUSKAL (DSU). Duyệt cạnh theo trọng số tăng dần.', 'info');
    setCanvasStatus('Kruskal: Bấm "Từng bước" hoặc kéo thả đỉnh để điều chỉnh mạng lưới.');
  } else {
    const startNodeObj = simNodes.find(n => n.id === simState.primStartNode);
    addSimLog(`Thuật toán: PRIM. Đỉnh xuất phát hiện tại: ${startNodeObj ? startNodeObj.name : simState.primStartNode}.`, 'info');
    setCanvasStatus(`Prim: Đang xuất phát từ ${simState.primStartNode}. Click vào đỉnh khác để đổi đỉnh bắt đầu.`);
  }

  renderGraph();
}

function dsuFind(u) {
  if (simState.dsuParent[u] === u) return u;
  return simState.dsuParent[u] = dsuFind(simState.dsuParent[u]);
}

function dsuUnion(u, v) {
  const rootU = dsuFind(u);
  const rootV = dsuFind(v);
  if (rootU !== rootV) {
    simState.dsuParent[rootU] = rootV;
    return true;
  }
  return false;
}

function runSimStep() {
  if (simState.algo === 'kruskal') {
    stepKruskal();
  } else {
    stepPrim();
  }
}

function stepKruskal() {
  if (simState.stepIndex >= simState.sortedEdges.length || simState.mstEdges.length === simNodes.length - 1) {
    addSimLog('Kruskal hoàn tất. Mạng lưới đã đạt cấu trúc MST tối ưu.', 'accept');
    setCanvasStatus('Hoàn thành: Toàn bộ 6 đỉnh đã được liên thông với chi phí nhỏ nhất.');
    if (simState.autoInterval) toggleSimAuto();
    return;
  }

  const edge = simState.sortedEdges[simState.stepIndex];
  simState.stepIndex++;

  const rootU = dsuFind(edge.u);
  const rootV = dsuFind(edge.v);

  if (rootU !== rootV) {
    dsuUnion(edge.u, edge.v);
    simState.mstEdges.push(edge);
    simState.totalWeight += edge.w;
    addSimLog(`[CHẤP NHẬN] (${edge.u} - ${edge.v}, w=${edge.w}) nối 2 cụm độc lập.`, 'accept');
    setCanvasStatus(`Chấp nhận tuyến (${edge.u} ↔ ${edge.v}, ${edge.w} km) vào cây.`);
  } else {
    addSimLog(`[LOẠI BỎ] (${edge.u} - ${edge.v}, w=${edge.w}) nối 2 đỉnh cùng cụm (tạo chu trình).`, 'reject');
    setCanvasStatus(`Từ chối tuyến (${edge.u} ↔ ${edge.v}) vì tạo chu trình khép kín.`);
  }

  updateSimStats();
  renderGraph(edge);
}

function stepPrim() {
  if (simState.mstEdges.length === simNodes.length - 1) {
    addSimLog('Prim hoàn tất. Đã liên thông toàn bộ các đỉnh.', 'accept');
    setCanvasStatus('Hoàn thành: Đã kết nối tất cả các trạm giao vận.');
    if (simState.autoInterval) toggleSimAuto();
    return;
  }

  let candidateEdge = null;
  let minW = Infinity;

  simEdges.forEach(e => {
    const uIn = simState.visitedPrim.has(e.u);
    const vIn = simState.visitedPrim.has(e.v);

    if ((uIn && !vIn) || (!uIn && vIn)) {
      if (e.w < minW) {
        minW = e.w;
        candidateEdge = e;
      }
    }
  });

  if (candidateEdge) {
    simState.mstEdges.push(candidateEdge);
    simState.totalWeight += candidateEdge.w;
    simState.visitedPrim.add(candidateEdge.u);
    simState.visitedPrim.add(candidateEdge.v);
    addSimLog(`[PRIM NẠP] Cạnh rẻ nhất qua lát cắt: (${candidateEdge.u} - ${candidateEdge.v}, w=${candidateEdge.w}).`, 'accept');
    setCanvasStatus(`Prim kết nạp đỉnh mới qua cạnh (${candidateEdge.u} ↔ ${candidateEdge.v}, ${candidateEdge.w} km).`);
    updateSimStats();
    renderGraph(candidateEdge);
  } else {
    addSimLog('Không còn cạnh nối ngoài lát cắt.', 'info');
  }
}

function toggleSimAuto() {
  const autoBtn = document.getElementById('simAutoBtn');
  if (simState.autoInterval) {
    clearInterval(simState.autoInterval);
    simState.autoInterval = null;
    if (autoBtn) autoBtn.textContent = 'Tự động';
  } else {
    if (autoBtn) autoBtn.textContent = 'Dừng';
    simState.autoInterval = setInterval(runSimStep, 1000);
  }
}

function updateSimStats() {
  const edgesCountEl = document.getElementById('simEdgesCount');
  const weightValEl = document.getElementById('simWeightVal');
  const compsValEl = document.getElementById('simCompsVal');

  if (edgesCountEl) edgesCountEl.textContent = `${simState.mstEdges.length} / ${simNodes.length - 1}`;
  if (weightValEl) weightValEl.textContent = simState.totalWeight.toFixed(1);

  if (compsValEl) {
    if (simState.algo === 'kruskal') {
      const roots = new Set(simNodes.map(n => dsuFind(n.id)));
      compsValEl.textContent = roots.size;
    } else {
      compsValEl.textContent = `${simNodes.length - simState.visitedPrim.size + 1}`;
    }
  }
}

function addSimLog(msg, type = 'info') {
  const logContent = document.getElementById('simLogContent');
  if (logContent) {
    const item = document.createElement('div');
    item.className = `log-item ${type}`;
    item.textContent = `> ${msg}`;
    logContent.appendChild(item);
    logContent.scrollTop = logContent.scrollHeight;
  }
}

function clearSimLog() {
  const logContent = document.getElementById('simLogContent');
  if (logContent) logContent.innerHTML = '';
}

function setCanvasStatus(text) {
  const statusEl = document.getElementById('simCanvasStatus');
  if (statusEl) statusEl.textContent = text;
}

// Convert screen pointer event to SVG coordinates
function getSvgPoint(e, svg) {
  const pt = svg.createSVGPoint();
  if (e.touches && e.touches[0]) {
    pt.x = e.touches[0].clientX;
    pt.y = e.touches[0].clientY;
  } else {
    pt.x = e.clientX;
    pt.y = e.clientY;
  }
  return pt.matrixTransform(svg.getScreenCTM().inverse());
}

// Setup Dragging & Pointer Listeners
function setupCanvasDragging() {
  const svg = document.getElementById('simSvg');
  if (!svg) return;

  function onPointerMove(e) {
    if (dragInfo.node) {
      e.preventDefault();
      const pt = getSvgPoint(e, svg);
      // Constrain within SVG bounds
      dragInfo.node.x = Math.max(25, Math.min(495, pt.x - dragInfo.offsetX));
      dragInfo.node.y = Math.max(25, Math.min(355, pt.y - dragInfo.offsetY));
      renderGraph();
      setCanvasStatus(`Đang di chuyển [ ${dragInfo.node.name} ] tới (${Math.round(dragInfo.node.x)}, ${Math.round(dragInfo.node.y)})`);
    }
  }

  function onPointerUp() {
    if (dragInfo.node) {
      setCanvasStatus(`Đã đặt đỉnh [ ${dragInfo.node.name} ] tại vị trí mới.`);
      dragInfo.node = null;
      renderGraph();
    }
  }

  svg.addEventListener('mousemove', onPointerMove);
  svg.addEventListener('touchmove', onPointerMove, { passive: false });

  window.addEventListener('mouseup', onPointerUp);
  window.addEventListener('touchend', onPointerUp);
}

// Render Interactive Graph
function renderGraph(activeEdge = null) {
  const svg = document.getElementById('simSvg');
  if (!svg) return;
  svg.innerHTML = '';

  const nodeMap = {};
  simNodes.forEach(n => nodeMap[n.id] = n);

  // 1. Draw Edges
  simEdges.forEach(e => {
    const u = nodeMap[e.u];
    const v = nodeMap[e.v];
    const isMst = simState.mstEdges.some(me => (me.u === e.u && me.v === e.v) || (me.u === e.v && me.v === e.u));
    const isActive = activeEdge && ((activeEdge.u === e.u && activeEdge.v === e.v) || (activeEdge.u === e.v && activeEdge.v === e.u));
    const isIncidentToHovered = simState.hoveredNode && (e.u === simState.hoveredNode || e.v === simState.hoveredNode);
    const isHovered = simState.hoveredEdge && (simState.hoveredEdge.u === e.u && simState.hoveredEdge.v === e.v);

    let strokeColor = 'rgba(255, 255, 255, 0.12)';
    let strokeWidth = '1.5';
    let strokeDash = 'none';

    if (isMst) {
      strokeColor = '#34d399'; // Minimalist Emerald
      strokeWidth = '2.8';
    } else if (isActive) {
      strokeColor = '#ffffff';
      strokeWidth = '2.2';
      strokeDash = '4,4';
    } else if (isHovered || isIncidentToHovered) {
      strokeColor = 'rgba(255, 255, 255, 0.4)';
      strokeWidth = '2';
    }

    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', u.x);
    line.setAttribute('y1', u.y);
    line.setAttribute('x2', v.x);
    line.setAttribute('y2', v.y);
    line.setAttribute('stroke', strokeColor);
    line.setAttribute('stroke-width', strokeWidth);
    if (strokeDash !== 'none') line.setAttribute('stroke-dasharray', strokeDash);
    line.setAttribute('class', 'svg-edge');

    // Edge interactions
    line.addEventListener('mouseenter', () => {
      simState.hoveredEdge = e;
      setCanvasStatus(`Tuyến đường ${e.u} (${u.name}) ↔ ${e.v} (${v.name}) | Khoảng cách: ${e.w} km | ${isMst ? 'ĐÃ NẰM TRONG MST' : 'Chưa được kết nạp'}`);
      line.setAttribute('stroke', '#ffffff');
      line.setAttribute('stroke-width', '3');
    });

    line.addEventListener('mouseleave', () => {
      simState.hoveredEdge = null;
      renderGraph(activeEdge);
    });

    line.addEventListener('click', (ev) => {
      ev.stopPropagation();
      addSimLog(`Tuyến ${e.u} ↔ ${e.v} (Trọng số: ${e.w} km). Trạng thái: ${isMst ? 'Đã trong cây MST' : 'Không thuộc MST / Chưa xét'}`, 'info');
      setCanvasStatus(`Chi tiết tuyến ${e.u} ↔ ${e.v}: Chi phí = ${e.w}`);
    });

    svg.appendChild(line);

    // Edge Weight Label
    const midX = (u.x + v.x) / 2;
    const midY = (u.y + v.y) / 2;

    const bgRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    bgRect.setAttribute('x', midX - 12);
    bgRect.setAttribute('y', midY - 14);
    bgRect.setAttribute('width', '24');
    bgRect.setAttribute('height', '12');
    bgRect.setAttribute('fill', '#090a0d');
    bgRect.setAttribute('opacity', '0.75');
    bgRect.setAttribute('rx', '2');
    svg.appendChild(bgRect);

    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', midX);
    text.setAttribute('y', midY - 5);
    text.setAttribute('fill', isMst ? '#ffffff' : '#757d8f');
    text.setAttribute('font-size', '9.5');
    text.setAttribute('font-family', 'JetBrains Mono');
    text.setAttribute('font-weight', isMst ? '600' : '400');
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('class', 'edge-weight-label');
    text.textContent = `${e.w}`;
    svg.appendChild(text);
  });

  // 2. Draw Nodes
  simNodes.forEach(n => {
    const isPrimStart = (simState.algo === 'prim' && n.id === simState.primStartNode);
    const inMst = (simState.algo === 'prim' && simState.visitedPrim.has(n.id));
    const isDragging = (dragInfo.node && dragInfo.node.id === n.id);

    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('transform', `translate(${n.x}, ${n.y})`);
    g.setAttribute('class', `svg-node ${isDragging ? 'is-dragging' : ''} ${isPrimStart ? 'is-prim-start' : ''}`);

    // Outer circle
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('r', isPrimStart ? '18' : '16');

    let fill = '#13161f';
    let stroke = 'rgba(255, 255, 255, 0.2)';

    if (isPrimStart) {
      stroke = '#3b82f6';
      fill = '#101726';
    } else if (n.type === 'hub') {
      stroke = '#3b82f6';
      fill = '#101726';
    } else if (inMst) {
      stroke = '#34d399';
    }

    circle.setAttribute('fill', fill);
    circle.setAttribute('stroke', stroke);
    circle.setAttribute('stroke-width', isPrimStart ? '2.5' : '1.5');
    g.appendChild(circle);

    // Node ID text
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('y', '4');
    text.setAttribute('fill', '#ffffff');
    text.setAttribute('font-size', '9.5');
    text.setAttribute('font-weight', '500');
    text.setAttribute('font-family', 'JetBrains Mono');
    text.setAttribute('text-anchor', 'middle');
    text.textContent = n.id;
    g.appendChild(text);

    // Node Name label below
    const nameText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    nameText.setAttribute('y', '27');
    nameText.setAttribute('fill', '#8892a4');
    nameText.setAttribute('font-size', '9.5');
    nameText.setAttribute('font-family', 'Inter');
    nameText.setAttribute('text-anchor', 'middle');
    nameText.textContent = n.name;
    g.appendChild(nameText);

    // Prim Start Badge if applicable
    if (isPrimStart) {
      const startBadge = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      startBadge.setAttribute('y', '-22');
      startBadge.setAttribute('fill', '#93c5fd');
      startBadge.setAttribute('font-size', '8');
      startBadge.setAttribute('font-family', 'JetBrains Mono');
      startBadge.setAttribute('font-weight', '600');
      startBadge.setAttribute('text-anchor', 'middle');
      startBadge.textContent = 'PRIM START';
      g.appendChild(startBadge);
    }

    // Node Drag Events
    function startDrag(e) {
      e.stopPropagation();
      const pt = getSvgPoint(e, svg);
      dragInfo.node = n;
      dragInfo.offsetX = pt.x - n.x;
      dragInfo.offsetY = pt.y - n.y;
      renderGraph();
    }

    g.addEventListener('mousedown', startDrag);
    g.addEventListener('touchstart', startDrag, { passive: false });

    // Node Hover Events
    g.addEventListener('mouseenter', () => {
      simState.hoveredNode = n.id;
      if (simState.algo === 'prim') {
        setCanvasStatus(`Đỉnh ${n.name} (${n.id}) | Click để chọn làm đỉnh xuất phát Prim`);
      } else {
        const root = dsuFind(n.id);
        setCanvasStatus(`Đỉnh ${n.name} (${n.id}) | Thuộc cụm DSU gốc: [ ${root} ] | Kéo thả để di chuyển`);
      }
    });

    g.addEventListener('mouseleave', () => {
      simState.hoveredNode = null;
    });

    // Node Click Event
    g.addEventListener('click', (e) => {
      e.stopPropagation();
      if (simState.algo === 'prim') {
        simState.primStartNode = n.id;
        resetSimState();
        addSimLog(`Đã chuyển đỉnh xuất phát Prim sang: ${n.name} (${n.id}).`, 'info');
        setCanvasStatus(`Đã chọn [ ${n.name} ] làm đỉnh xuất phát cho Prim.`);
      } else {
        addSimLog(`Đỉnh: ${n.name} (${n.id}). Cụm đại diện DSU hiện tại: ${dsuFind(n.id)}.`, 'info');
      }
    });

    svg.appendChild(g);
  });
}

// Start everything on DOM ready
document.addEventListener('DOMContentLoaded', initPresentation);
