(async function () {
  if (!window.PDF_URL || !window.pdfjsLib) return;

  const pdfjsLib = window.pdfjsLib;
  pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';

  const canvas = document.getElementById('pdfCanvas');
  const textLayer = document.getElementById('textLayer');
  const pageInfo = document.getElementById('pageInfo');
  const pageNumberInput = document.getElementById('pageNumberInput');
  const selectedTextField = document.getElementById('selectedText');
  const prevBtn = document.getElementById('prevPage');
  const nextBtn = document.getElementById('nextPage');
  const zoomInBtn = document.getElementById('zoomIn');
  const zoomOutBtn = document.getElementById('zoomOut');
  const fitBtn = document.getElementById('fitWidth');
  const status = document.getElementById('readerStatus');
  const viewerShell = document.getElementById('pdfPageShell');

  if (!canvas || !textLayer || !viewerShell) return;

  const ctx = canvas.getContext('2d', { alpha: false });
  const pdf = await pdfjsLib.getDocument(window.PDF_URL).promise;
  let pageNum = 1;
  let scale = 1.35;
  let renderToken = 0;

  function setStatus(message) {
    if (status) status.textContent = message;
  }

  function clearSelection() {
    const selection = window.getSelection ? window.getSelection() : null;
    if (selection && selection.rangeCount > 0) selection.removeAllRanges();
  }

  function updateSelectedText() {
    const selection = window.getSelection ? window.getSelection() : null;
    if (!selection) return;
    const selected = String(selection).replace(/\s+/g, ' ').trim();
    if (selected) {
      selectedTextField.value = selected;
      pageNumberInput.value = pageNum;
    }
  }

  async function renderTextLayer(page, viewport) {
    const textContent = await page.getTextContent();
    textLayer.innerHTML = '';
    textLayer.style.width = `${viewport.width}px`;
    textLayer.style.height = `${viewport.height}px`;

    for (const item of textContent.items) {
      const tx = pdfjsLib.Util.transform(viewport.transform, item.transform);
      const angle = Math.atan2(tx[1], tx[0]);
      const fontHeight = Math.hypot(tx[2], tx[3]);
      const span = document.createElement('span');
      span.textContent = item.str;
      span.dir = item.dir || 'ltr';
      span.style.left = `${tx[4]}px`;
      span.style.top = `${tx[5] - fontHeight}px`;
      span.style.fontSize = `${fontHeight}px`;
      span.style.fontFamily = item.fontName || 'sans-serif';
      span.style.transform = `rotate(${angle}rad)`;
      if (item.width) {
        span.style.width = `${item.width * viewport.scale}px`;
      }
      textLayer.appendChild(span);
      if (!item.hasEOL) {
        span.appendChild(document.createTextNode(' '));
      }
    }
  }

  async function renderPage(num) {
    const token = ++renderToken;
    setStatus('Rendering page...');
    clearSelection();

    const page = await pdf.getPage(num);
    const viewport = page.getViewport({ scale });

    canvas.width = Math.floor(viewport.width * window.devicePixelRatio);
    canvas.height = Math.floor(viewport.height * window.devicePixelRatio);
    canvas.style.width = `${viewport.width}px`;
    canvas.style.height = `${viewport.height}px`;
    textLayer.style.width = `${viewport.width}px`;
    textLayer.style.height = `${viewport.height}px`;
    viewerShell.style.width = `${viewport.width}px`;
    viewerShell.style.height = `${viewport.height}px`;

    ctx.setTransform(window.devicePixelRatio, 0, 0, window.devicePixelRatio, 0, 0);

    await page.render({
      canvasContext: ctx,
      viewport,
    }).promise;

    if (token !== renderToken) return;

    await renderTextLayer(page, viewport);

    pageInfo.textContent = `Page ${num} / ${pdf.numPages}`;
    pageNumberInput.value = num;
    prevBtn.disabled = num <= 1;
    nextBtn.disabled = num >= pdf.numPages;
    setStatus('Select text directly on the page to save a statement.');
  }

  async function goToPage(nextPage) {
    const safePage = Math.min(Math.max(nextPage, 1), pdf.numPages);
    if (safePage === pageNum && renderToken !== 0) return;
    pageNum = safePage;
    await renderPage(pageNum);
  }

  function fitToWidth() {
    const container = document.getElementById('pdfContainer');
    if (!container) return;
    pdf.getPage(pageNum).then((page) => {
      const unscaled = page.getViewport({ scale: 1 });
      const availableWidth = Math.max(container.clientWidth - 32, 320);
      scale = availableWidth / unscaled.width;
      renderPage(pageNum);
    });
  }

  prevBtn.addEventListener('click', () => goToPage(pageNum - 1));
  nextBtn.addEventListener('click', () => goToPage(pageNum + 1));

  if (zoomInBtn) {
    zoomInBtn.addEventListener('click', () => {
      scale = Math.min(scale + 0.15, 3);
      renderPage(pageNum);
    });
  }

  if (zoomOutBtn) {
    zoomOutBtn.addEventListener('click', () => {
      scale = Math.max(scale - 0.15, 0.75);
      renderPage(pageNum);
    });
  }

  if (fitBtn) {
    fitBtn.addEventListener('click', fitToWidth);
  }

  textLayer.addEventListener('mouseup', updateSelectedText);
  textLayer.addEventListener('keyup', updateSelectedText);
  document.addEventListener('selectionchange', () => {
    const activeSelection = window.getSelection ? String(window.getSelection()).trim() : '';
    if (!activeSelection && document.activeElement !== selectedTextField) return;
    if (activeSelection) updateSelectedText();
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth < 1100) {
      fitToWidth();
    }
  });

  await goToPage(pageNum);
})();
