document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const uploadBox = document.querySelector('.upload-box');
    const fileNameDisplay = document.getElementById('file-name');
    const upscaleBtn = document.getElementById('upscale-btn');
    const resultSection = document.getElementById('result-section');
    const loader = document.getElementById('loader');

    // Elements for result
    const originalImg = document.getElementById('original-img');
    const upscaledImg = document.getElementById('upscaled-img');
    const downloadLink = document.getElementById('download-link');
    const resetBtn = document.getElementById('reset-btn');

    let selectedFile = null;

    // Upload interactions
    uploadBox.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', () => uploadBox.classList.remove('dragover'));

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        handleFile(e.dataTransfer.files[0]);
    });

    function handleFile(file) {
        if (!file) return;
        if (!['image/jpeg', 'image/png'].includes(file.type)) {
            alert('Only JPG and PNG are supported.');
            return;
        }
        selectedFile = file;
        fileNameDisplay.textContent = file.name;
        fileNameDisplay.classList.remove('hidden');
        upscaleBtn.disabled = false;

        // Preview original
        const reader = new FileReader();
        reader.onload = (e) => {
            originalImg.src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
    // Upscale Logic
    upscaleBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        const mode = document.querySelector('input[name="mode"]:checked').value;
        const scale = document.querySelector('input[name="scale"]:checked').value;

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('mode', mode);
        formData.append('scale', scale);

        // UI State
        upscaleBtn.disabled = true;
        loader.classList.remove('hidden');
        resultSection.classList.add('hidden');

        try {
            const response = await fetch('/upscale', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Upscaling failed');
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            // Update UI
            upscaledImg.src = url;
            downloadLink.href = url;

            resultSection.classList.remove('hidden');

            // Scroll to result
            resultSection.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error(error);
            alert('Error: ' + error.message);
        } finally {
            loader.classList.add('hidden');
            upscaleBtn.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        fileInput.value = '';
        selectedFile = null;
        fileNameDisplay.classList.add('hidden');
        upscaleBtn.disabled = true;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
