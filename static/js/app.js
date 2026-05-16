(() => {
  'use strict';

  const CATEGORIES = {
    Battery:   { emoji: '🔋', tip: 'Never throw batteries in regular trash. Take them to a designated hazardous waste collection point.', bin: '#ef4444', binName: 'Red (Hazardous)' },
    Cardboard: { emoji: '📦', tip: 'Flatten all boxes to save space. Keep cardboard dry and free of food grease.', bin: '#3b82f6', binName: 'Blue (Recycling)' },
    Clothes:   { emoji: '👕', tip: 'Donate wearable clothes. Worn-out textiles go to fabric recycling points.', bin: '#8b5cf6', binName: 'Purple (Textile)' },
    Glass:     { emoji: '🍾', tip: 'Rinse glass containers. Separate by color if required by your local program.', bin: '#22c55e', binName: 'Green (Glass)' },
    Metal:     { emoji: '🥫', tip: 'Rinse cans and crush them. Aluminum and steel are infinitely recyclable!', bin: '#f59e0b', binName: 'Yellow (Metal)' },
    Paper:     { emoji: '📄', tip: 'Keep paper clean and dry. Avoid recycling wax-coated or laminated paper.', bin: '#3b82f6', binName: 'Blue (Recycling)' },
    Plastic:   { emoji: '🧴', tip: 'Rinse containers and remove caps. Check the recycling number on the bottom.', bin: '#f97316', binName: 'Orange (Plastic)' },
  };

  const fileInput      = document.getElementById('file-input');
  const dropZone       = document.getElementById('drop-zone');
  const dropZoneInner  = document.getElementById('drop-zone-inner');
  const previewWrapper = document.getElementById('preview-wrapper');
  const previewImg     = document.getElementById('preview-img');
  const previewRemove  = document.getElementById('preview-remove');
  const classifyBtn    = document.getElementById('classify-btn');
  const classifyLabel  = document.getElementById('classify-label');
  const classifySpinner= document.getElementById('classify-spinner');
  const emptyState     = document.getElementById('empty-state');
  const resultContent  = document.getElementById('result-content');
  const resultLabel    = document.getElementById('result-label');
  const categoryIcon   = document.getElementById('category-icon');
  const barFill        = document.getElementById('bar-fill');
  const confidencePct  = document.getElementById('confidence-pct');
  const disposalTip    = document.getElementById('disposal-tip');
  const disposalIcon   = document.getElementById('disposal-icon');
  const binDot         = document.getElementById('bin-dot');
  const binName        = document.getElementById('bin-name');
  const resetBtn       = document.getElementById('reset-btn');
  const toast          = document.getElementById('toast');
  const categoriesGrid = document.getElementById('categories-grid');

  let currentFile = null;

  /* ── Categories grid ── */
  Object.entries(CATEGORIES).forEach(([name, data]) => {
    const card = document.createElement('div');
    card.className = 'cat-card';
    card.dataset.category = name;
    card.innerHTML = `<div class="cat-emoji">${data.emoji}</div><div class="cat-name">${name}</div>`;
    categoriesGrid.appendChild(card);
  });

  function showToast(msg, type = '') {
    toast.textContent = msg;
    toast.className = 'toast show' + (type ? ' ' + type : '');
    setTimeout(() => { toast.className = 'toast'; }, 3500);
  }

  function showPreview(src) {
    previewImg.src = src;
    dropZoneInner.hidden = true;
    previewWrapper.hidden = false;
    classifyBtn.disabled = false;
    classifyLabel.textContent = '🔍 Classify Image';
  }

  function clearPreview() {
    previewImg.src = '';
    dropZoneInner.hidden = false;
    previewWrapper.hidden = true;
    classifyBtn.disabled = true;
    classifyLabel.textContent = 'Select an image first';
    currentFile = null;
    fileInput.value = '';
  }

  function showResult(label, confidence) {
    const data = CATEGORIES[label] || { emoji: '♻️', tip: 'Dispose responsibly.', bin: '#6b7280', binName: 'General Waste' };
    const pct = Math.round(confidence * 100);
    emptyState.hidden = true;
    resultContent.hidden = false;
    categoryIcon.textContent = data.emoji;
    resultLabel.textContent = label;
    barFill.style.width = pct + '%';
    confidencePct.textContent = pct + '%';
    disposalIcon.textContent = data.emoji;
    disposalTip.textContent = data.tip;
    binDot.style.background = data.bin;
    binName.textContent = data.binName;
    document.querySelectorAll('.cat-card').forEach(c => c.classList.toggle('active', c.dataset.category === label));
  }

async function classify(file) {
    if (!MODEL_LOADED) {
      showToast('⚠️ Model is not loaded on the server.', 'error');
      return;
    }

    try {
      const fd = new FormData();
      fd.append('image', file);

      const res = await fetch('/predict', { method: 'POST', body: fd });
      const body = await res.json();
      
      if (!res.ok) {
        showToast('❌ ' + (body.error || 'Prediction failed'), 'error');
      } else {
        showResult(body.label, body.confidence);
        showToast('✅ Classification complete!', 'success');
      }
    } catch (err) {
      showToast('❌ Network error: ' + err.message, 'error');
    }
  }

  fileInput.addEventListener('change', e => {
    const f = e.target.files[0];
    if (!f) return;
    currentFile = f;
    showPreview(URL.createObjectURL(f));
  });

  dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const f = e.dataTransfer.files[0];
    if (f && f.type.startsWith('image/')) {
      currentFile = f;
      showPreview(URL.createObjectURL(f));
    }
  });

  dropZone.addEventListener('click', () => { if (previewWrapper.hidden) fileInput.click(); });
  previewRemove.addEventListener('click', e => { e.stopPropagation(); clearPreview(); });
  classifyBtn.addEventListener('click', () => { if (currentFile) classify(currentFile); });
  resetBtn.addEventListener('click', clearPreview);
})();