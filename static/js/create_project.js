let currentSlide = 0
const slider = document.getElementById('slider')
const slides = document.querySelectorAll('#slider .section-tab')
const totalSlides = slides.length
const prevBtn = document.getElementById('prevBtn')
const nextBtn = document.getElementById('nextBtn')

// Set slider width dynamically based on number of slides
function setSliderWidth() {
    const containerWidth = document.getElementById('slider-container').offsetWidth
    slider.style.width = `${containerWidth * totalSlides}px`
    slides.forEach((slide) => {
        slide.style.width = `${containerWidth}px`
    })
}

function updateSlide() {
    const slideWidth = document.getElementById('slider-container').offsetWidth
    slider.style.transform = `translateX(-${slideWidth * currentSlide}px)`

    prevBtn.disabled = currentSlide === 0
    nextBtn.disabled = currentSlide === totalSlides - 1

    // Highlight corresponding menu-tab
    const tabs = document.querySelectorAll('.menu-tab')
    tabs.forEach((tab, index) => {
        if (index === currentSlide) {
            tab.classList.remove('bg-white')
            tab.classList.add('bg-gray-200')
        } else {
            tab.classList.remove('bg-gray-200')
            tab.classList.add('bg-white')
        }
    })
}

function showSection(sectionId) {
    if (!areCurrentSlideFieldsValid()) {
        showMessage({
            title: 'Validation Error',
            content: 'Please fill in all required fields before proceeding.'
        })
        return
    }

    const sectionIndex = Array.from(slides).findIndex((slide) => slide.id === sectionId)
    if (sectionIndex !== -1) {
        currentSlide = sectionIndex
        updateSlide()
    }
}

function areCurrentSlideFieldsValid() {
    const currentSection = slides[currentSlide]
    const inputs = currentSection.querySelectorAll('input[required], textarea[required], select[required]')
    let isValid = true

    inputs.forEach((input) => {
        if (!input.value.trim()) {
            input.classList.add('border-red-500')
            isValid = false
        } else {
            input.classList.remove('border-red-500')
        }
    })

    const start = new Date(document.getElementById("start_date").value);
    const end = new Date(document.getElementById("end_date").value);
    const delivery = new Date(document.getElementById("delivery_date").value);

    if (start < new Date(today)) {
        showMessage({
            title: 'Validation Error',
            content: 'Start date cannot be before today.'
        })
        e.preventDefault();
    } else if (end <= start) {
        showMessage({
            title: 'Validation Error',
            content: 'End date must be after the start date.'
        })
        e.preventDefault();
    } else if (delivery <= start) {
        showMessage({
            title: 'Validation Error',
            content: 'Delivery date must be after the start date.'
        })
        e.preventDefault();
    }
    
    return isValid
}

nextBtn.addEventListener('click', () => {
    if (!areCurrentSlideFieldsValid()) {
        showMessage({
            title: 'Validation Error',
            content: 'Please fill in all required fields before proceeding.'
        })
        return
    }
    if (currentSlide < totalSlides - 1) {
        currentSlide++
        updateSlide()
    }
})

nextBtn.addEventListener('focus', (e) => {
    if (!areCurrentSlideFieldsValid()) {
        e.preventDefault()
        nextBtn.blur()
    }
})

function trapFocusInCurrentSlide(e) {
    const focusableElements = slides[currentSlide].querySelectorAll(
        'input, textarea, select, button, [tabindex]:not([tabindex="-1"])'
    )

    const firstEl = focusableElements[0]
    const lastEl = focusableElements[focusableElements.length - 1]

    if (e.key === 'Tab') {
        if (e.shiftKey) {
            if (document.activeElement === firstEl) {
                e.preventDefault()
                lastEl.focus()
            }
        } else {
            if (document.activeElement === lastEl) {
                e.preventDefault()
                firstEl.focus()
            }
        }
    }
}

document.addEventListener('keydown', (e) => {
    trapFocusInCurrentSlide(e)
})

prevBtn.addEventListener('click', () => {
    if (currentSlide > 0) {
        currentSlide--
        updateSlide()
    }
})

window.addEventListener('resize', () => {
    setSliderWidth()
    updateSlide()
})

window.onload = () => {
    setSliderWidth()
    updateSlide()
}

const campaignCoverInput = document.getElementById('campaign_cover_input')
const campaignCoverSpan = document.getElementById('campaign_cover_text')
const campaignGalleryInput = document.getElementById('campaign_gallery_input')
const campaignGallerySpan = document.getElementById('campaign_gallery_text')

campaignCoverInput.addEventListener('change', function () {
    if (campaignCoverInput.files.length > 0) {
        campaignCoverSpan.textContent = campaignCoverInput.files[0].name
    } else {
        campaignCoverSpan.textContent = 'No file selected'
    }
})

campaignGalleryInput.addEventListener('change', function () {
    if (campaignGalleryInput.files.length > 0) {
        campaignGallerySpan.textContent = campaignGalleryInput.files[0].name
    } else {
        campaignGallerySpan.textContent = 'No file selected'
    }
})

const dropdownButton = document.getElementById('dropdown-button')
const dropdownOptions = document.getElementById('dropdown-options')
const dropdownSelected = document.getElementById('dropdown-selected')
const selectedCategoryInput = document.getElementById('selected-category')

dropdownButton.addEventListener('click', () => {
    dropdownOptions.classList.toggle('hidden')
})

dropdownOptions.querySelectorAll('li').forEach((item) => {
    item.addEventListener('click', () => {
        const value = item.getAttribute('data-value')
        dropdownSelected.textContent = value
        selectedCategoryInput.value = value
        dropdownOptions.classList.add('hidden')
    })
})

// Optional: Close dropdown if clicked outside
document.addEventListener('click', (e) => {
    if (!dropdownButton.contains(e.target) && !dropdownOptions.contains(e.target)) {
        dropdownOptions.classList.add('hidden')
    }
})

function showMessage({ title = '', content = '' }) {
    const messageOverlay = document.getElementById('message-overlay')
    const messageTitle = document.getElementById('message-title')
    const messageContent = document.getElementById('message-content')
    const messageButton = document.getElementById('message-button')

    // Reset previous styles and content
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