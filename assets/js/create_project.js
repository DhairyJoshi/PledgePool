// Enhanced Campaign Slider Validation Script
let currentSlide = 0;
const slider = document.getElementById('slider');
const slides = document.querySelectorAll('#slider .section-tab');
const totalSlides = slides.length;
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

function setSliderWidth() {
    const containerWidth = document.getElementById('slider-container').offsetWidth;
    slider.style.width = `${containerWidth * totalSlides}px`;
    slides.forEach(slide => slide.style.width = `${containerWidth}px`);
}

function updateSlide() {
    const slideWidth = document.getElementById('slider-container').offsetWidth;
    slider.style.transform = `translateX(-${slideWidth * currentSlide}px)`;
    prevBtn.disabled = currentSlide === 0;
    nextBtn.disabled = currentSlide === totalSlides - 1;
    document.querySelectorAll('.menu-tab').forEach((tab, i) => {
        tab.classList.toggle('bg-white', i !== currentSlide);
        tab.classList.toggle('bg-gray-200', i === currentSlide);
    });
}

function showSection(sectionId) {
    const sectionIndex = [...slides].findIndex(slide => slide.id === sectionId);
    console.log(sectionIndex, "ss")
    if (sectionIndex === -1) return;

    // Only run validation if moving forward
    if (sectionIndex > currentSlide && !areCurrentSlideFieldsValid()) {
        return showMessage({ title: 'Validation Error', content: 'Please fill in all required fields before proceeding.' });
    }

    // No validation needed if going back or staying on the same slide
    currentSlide = sectionIndex;
    updateSlide();
}


function areCurrentSlideFieldsValid() {
    const currentSection = slides[currentSlide];
    const inputs = currentSection.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        input.classList.toggle('border-red-500', !input.value.trim());
        if (!input.value.trim()) isValid = false;
    });

    const today = new Date().setHours(0, 0, 0, 0);
    const startEl = document.getElementById("start_date");
    const endEl = document.getElementById("end_date");
    const deliveryEl = document.getElementById("delivery_date");

    if (startEl && endEl && deliveryEl) {
        const start = new Date(startEl.value);
        const end = new Date(endEl.value);
        const delivery = new Date(deliveryEl.value);

        if (start < today) return showMessage({ title: 'Validation Error', content: 'Start date cannot be before today.' }), false;
        if (end <= start) return showMessage({ title: 'Validation Error', content: 'End date must be after the start date.' }), false;
        if (delivery <= start) return showMessage({ title: 'Validation Error', content: 'Delivery date must be after the start date.' }), false;
    }

    return isValid;
}

nextBtn.addEventListener('click', () => {
    if (!areCurrentSlideFieldsValid()) return showMessage({ title: 'Validation Error', content: 'Please fill in all required fields before proceeding.' });
    if (currentSlide < totalSlides - 1) currentSlide++, updateSlide();
});

nextBtn.addEventListener('focus', e => {
    if (!areCurrentSlideFieldsValid()) e.preventDefault(), nextBtn.blur();
});

document.addEventListener('keydown', e => {
    const focusable = slides[currentSlide].querySelectorAll('input, textarea, select, button, [tabindex]:not([tabindex="-1"])');
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === first) e.preventDefault(), last.focus();
        else if (!e.shiftKey && document.activeElement === last) e.preventDefault(), first.focus();
    }
});

prevBtn.addEventListener('click', () => {
    if (currentSlide > 0) currentSlide--, updateSlide();
});

window.addEventListener('resize', () => {
    setSliderWidth();
    updateSlide();
});

window.onload = () => {
    setSliderWidth();
    updateSlide();
};

const campaignCoverInput = document.getElementById('campaign_cover_input');
const campaignCoverText = document.getElementById('campaign_cover_text');
const campaignCoverContainer = document.getElementById('campaign_cover_container');
const campaignCoverClose = document.getElementById('campaign_cover_close');

campaignCoverInput.addEventListener('change', function () {
    if (this.files.length > 0) {
        campaignCoverContainer.style.display = "flex";
        campaignCoverText.textContent = this.files[0].name;
    } else {
        campaignCoverContainer.style.display = "none";
        campaignCoverText.textContent = 'No file selected';
    }
});

campaignCoverClose.addEventListener('click', function () {
    campaignCoverInput.value = "";
    campaignCoverContainer.style.display = "none";
    campaignCoverText.textContent = 'No file selected';
});

const campaignGalleryInput = document.getElementById('campaign_gallery_input');
const campaignGalleryTexts = document.getElementById('campaign_gallery_texts');
const campaignGalleryContainer = document.getElementById('campaign_gallery_container');

campaignGalleryInput.addEventListener('change', function () {
    if (this.files.length > 0) {
        campaignGalleryContainer.style.display = "flex";
        campaignGalleryTexts.innerHTML = '';
        Array.from(this.files).forEach(file => {
            const fileRow = document.createElement('div');
            fileRow.className = 'w-full h-auto flex justify-between items-center bg-[#ffddbe] rounded-lg px-4 py-2';
            const fileName = document.createElement('span');
            fileName.className = 'text-md';
            fileName.textContent = file.name;
            const removeBtn = document.createElement('div');
            removeBtn.className = 'w-8 h-8 cursor-pointer';
            removeBtn.innerHTML = '✕';
            removeBtn.addEventListener('click', () => fileRow.remove());
            fileRow.append(fileName, removeBtn);
            campaignGalleryTexts.appendChild(fileRow);
        });
    } else {
        campaignGalleryContainer.style.display = "none";
        campaignGalleryTexts.innerHTML = '';
    }
});

function showMessage({ title = '', content = '' }) {
    const messageOverlay = document.getElementById('message-overlay')
    const messageTitle = document.getElementById('message-title')
    const messageContent = document.getElementById('message-content')
    const messageButton = document.getElementById('message-button')

    // Reset previous styles and startEl 
    messageTitle.textContent = title
    messageContent.textContent = content
    messageButton.onclick = closeMessage


    messageOverlay.classList.remove('hidden')
    messageOverlay.classList.add('flex')
}

function closeMessage() {
    document.getElementById('message-overlay').classList.add('hidden')
    document.getElementById('message-overlay').classList.remove('flex')
}

const startDateInput = document.getElementById("start_date");
const endDateInput = document.getElementById("end_date");
const deliveryDateInput = document.getElementById("delivery_date");

// Set minimum start date to today
const today = new Date().toISOString().split("T")[0];
startDateInput.setAttribute("min", today);

// Update end date min dynamically when start date changes
startDateInput.addEventListener("change", () => {
    const startDate = startDateInput.value;
    endDateInput.setAttribute("min", startDate);
});

deliveryDateInput.addEventListener("change", () => {
    const startDate = startDateInput.value;
    deliveryDateInput.setAttribute("min", startDate);
});