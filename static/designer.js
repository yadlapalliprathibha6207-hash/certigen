let fields = [];
let activeFieldId = null;
let dragState = null;

const canvas = document.getElementById('canvas');
const fieldList = document.getElementById('fieldList');
const propertyPanel = document.getElementById('propertyPanel');
const genderToggle = document.getElementById('genderToggle');
const addFieldBtn = document.getElementById('addFieldBtn');
const saveLayoutBtn = document.getElementById('saveLayoutBtn');

function createField(name = 'New Field') {
    return {
        id: `field-${Date.now()}`,
        name,
        x: 250,
        y: 220,
        fontSize: 42,
        fontFamily: 'Times New Roman',
        color: '#000000',
        bold: false,
        italic: false,
        align: 'center'
    };
}

function renderFields() {
    fieldList.innerHTML = '';
    fields.forEach((field) => {
        const item = document.createElement('div');
        item.className = `field-item ${field.id === activeFieldId ? 'active' : ''}`;
        item.innerHTML = `
            <span>${field.name}</span>
            <span>⋮</span>
        `;
        item.addEventListener('click', () => selectField(field.id));
        fieldList.appendChild(item);
    });

    canvas.querySelectorAll('.canvas-field').forEach((el) => el.remove());
    fields.forEach((field) => {
        const el = document.createElement('div');
        el.className = `canvas-field ${field.id === activeFieldId ? 'active' : ''}`;
        el.dataset.fieldId = field.id;
        el.textContent = field.name;
        el.style.left = `${field.x}px`;
        el.style.top = `${field.y}px`;
        el.style.fontSize = `${field.fontSize}px`;
        el.style.fontFamily = field.fontFamily;
        el.style.color = field.color;
        el.style.fontWeight = field.bold ? 'bold' : 'normal';
        el.style.fontStyle = field.italic ? 'italic' : 'normal';
        el.style.textAlign = field.align;
        el.addEventListener('mousedown', (event) => startDrag(event, field.id));
        canvas.appendChild(el);
    });
}

function selectField(fieldId) {
    activeFieldId = fieldId;
    renderFields();
    renderProperties();
}

function renderProperties() {
    const field = fields.find((item) => item.id === activeFieldId);
    if (!field) {
        propertyPanel.innerHTML = '<p>Select a field to edit its style.</p>';
        return;
    }

    propertyPanel.innerHTML = `
        <label>Field</label>
        <input type="text" id="fieldName" value="${field.name}">
        <label>Font Size</label>
        <input type="number" id="fontSize" value="${field.fontSize}">
        <label>Font Family</label>
        <input type="text" id="fontFamily" value="${field.fontFamily}">
        <label>Color</label>
        <input type="color" id="fieldColor" value="${field.color}">
        <label>Alignment</label>
        <select id="fieldAlign">
            <option value="left" ${field.align === 'left' ? 'selected' : ''}>Left</option>
            <option value="center" ${field.align === 'center' ? 'selected' : ''}>Center</option>
            <option value="right" ${field.align === 'right' ? 'selected' : ''}>Right</option>
        </select>
        <label><input type="checkbox" id="boldToggle" ${field.bold ? 'checked' : ''}> Bold</label>
        <label><input type="checkbox" id="italicToggle" ${field.italic ? 'checked' : ''}> Italic</label>
        <button id="duplicateBtn">Duplicate Field</button>
        <button id="deleteBtn" style="background:#dc2626">Delete Field</button>
        <p class="hint">Changes update instantly on the preview.</p>
    `;

    document.getElementById('fieldName').addEventListener('input', (event) => {
        updateField(activeFieldId, { name: event.target.value });
    });
    document.getElementById('fontSize').addEventListener('input', (event) => {
        updateField(activeFieldId, { fontSize: Number(event.target.value) || 12 });
    });
    document.getElementById('fontFamily').addEventListener('input', (event) => {
        updateField(activeFieldId, { fontFamily: event.target.value });
    });
    document.getElementById('fieldColor').addEventListener('input', (event) => {
        updateField(activeFieldId, { color: event.target.value });
    });
    document.getElementById('fieldAlign').addEventListener('change', (event) => {
        updateField(activeFieldId, { align: event.target.value });
    });
    document.getElementById('boldToggle').addEventListener('change', (event) => {
        updateField(activeFieldId, { bold: event.target.checked });
    });
    document.getElementById('italicToggle').addEventListener('change', (event) => {
        updateField(activeFieldId, { italic: event.target.checked });
    });
    document.getElementById('duplicateBtn').addEventListener('click', () => duplicateField());
    document.getElementById('deleteBtn').addEventListener('click', () => deleteField());
}

function updateField(fieldId, changes) {
    fields = fields.map((field) => field.id === fieldId ? { ...field, ...changes } : field);
    renderFields();
    renderProperties();
    saveLayout();
}

function duplicateField() {
    const field = fields.find((item) => item.id === activeFieldId);
    if (!field) return;
    const duplicate = { ...field, id: `field-${Date.now()}`, x: field.x + 20, y: field.y + 20, name: `${field.name} Copy` };
    fields = [...fields, duplicate];
    activeFieldId = duplicate.id;
    renderFields();
    renderProperties();
    saveLayout();
}

function deleteField() {
    if (!activeFieldId) return;
    fields = fields.filter((field) => field.id !== activeFieldId);
    activeFieldId = fields[0]?.id || null;
    renderFields();
    renderProperties();
    saveLayout();
}

function startDrag(event, fieldId) {
    event.preventDefault();
    const field = fields.find((item) => item.id === fieldId);
    if (!field) return;
    activeFieldId = fieldId;
    dragState = {
        fieldId,
        startX: event.clientX,
        startY: event.clientY,
        originX: field.x,
        originY: field.y
    };
    renderFields();
    renderProperties();
}

function onMouseMove(event) {
    if (!dragState) return;
    const deltaX = event.clientX - dragState.startX;
    const deltaY = event.clientY - dragState.startY;
    updateField(dragState.fieldId, { x: dragState.originX + deltaX, y: dragState.originY + deltaY });
}

function stopDrag() {
    dragState = null;
}

function saveLayout() {
    fetch('/save_layout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fields, genderLogic: genderToggle.checked })
    }).catch(() => {});
}

addFieldBtn.addEventListener('click', () => {
    const name = window.prompt('Enter field name', 'New Field');
    if (!name) return;
    const field = createField(name);
    fields = [...fields, field];
    activeFieldId = field.id;
    renderFields();
    renderProperties();
    saveLayout();
});

saveLayoutBtn.addEventListener('click', () => {
    saveLayout();
    window.alert('Layout saved successfully.');
});

genderToggle.addEventListener('change', () => {
    saveLayout();
});

window.addEventListener('mousemove', onMouseMove);
window.addEventListener('mouseup', stopDrag);

fetch('/get_layout')
    .then((response) => response.json())
    .then((data) => {
        fields = data.fields || [];
        genderToggle.checked = data.genderLogic !== false;
        if (fields.length) {
            activeFieldId = fields[0].id;
        }
        renderFields();
        renderProperties();
    });