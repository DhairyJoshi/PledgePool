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
    const currentSection = slides[currentSlide];
    const inputs = currentSection.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach((input) => {
        if (!input.value.trim()) {
            input.classList.add('border-red-500');
            isValid = false;
        } else {
            input.classList.remove('border-red-500');
        }
    });

    // Date validation
    const today = new Date().setHours(0, 0, 0, 0); // normalize today's date
    const startEl = document.getElementById("start_date");
    const endEl = document.getElementById("end_date");
    const deliveryEl = document.getElementById("delivery_date");

    if (startEl && endEl && deliveryEl) {
        const start = new Date(startEl.value);
        const end = new Date(endEl.value);
        const delivery = new Date(deliveryEl.value);

        if (start < today) {
            showMessage({
                title: 'Validation Error',
                content: 'Start date cannot be before today.'
            });
            return false;
        } else if (end <= start) {
            showMessage({
                title: 'Validation Error',
                content: 'End date must be after the start date.'
            });
            return false;
        } else if (delivery <= start) {
            showMessage({
                title: 'Validation Error',
                content: 'Delivery date must be after the start date.'
            });
            return false;
        }
    }

    return isValid;
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
        currentSlide--;
        updateSlide();
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
const campaignCoverText = document.getElementById('campaign_cover_text')
const campaignCoverContainer = document.getElementById('campaign_cover_container')
const campaignCoverClose = document.getElementById('campaign_cover_close');
const campaignGalleryInput = document.getElementById('campaign_gallery_input')
const campaignGalleryTexts = document.getElementById('campaign_gallery_texts')
const campaignGalleryContainer = document.getElementById('campaign_gallery_container')
const campaignGalleryClose = document.getElementById('campaign_gallery_close');

campaignCoverInput.addEventListener('change', function () {
    if (campaignCoverInput.files.length > 0) {
        campaignCoverContainer.style.display = "flex";
        campaignCoverText.textContent = campaignCoverInput.files[0].name;
    } else {
        campaignCoverContainer.style.display = "none";
        campaignCoverText.textContent = 'No file selected';
    }
})

campaignCoverClose.addEventListener('click', function () {
  campaignCoverInput.value = "";
  campaignCoverContainer.style.display = "none";
  campaignCoverText.textContent = 'No file selected';
});

campaignGalleryInput.addEventListener('change', function () {
    if (campaignGalleryInput.files.length > 0) {
        campaignGalleryContainer.style.display = "flex";
        // Clear existing content
        campaignGalleryTexts.innerHTML = '';

        // Loop through all selected files and display their names
        Array.from(campaignGalleryInput.files).forEach((file, index) => {
            const fileNameContainer = document.createElement('div');
            fileNameContainer.classList.add('w-full', 'h-auto', 'flex', 'justify-between', 'items-center', 'bg-[#ffddbe]', 'rounded-lg', 'px-4', 'py-2');

            const fileNameSpan = document.createElement('span');
            fileNameSpan.classList.add('text-md');
            fileNameSpan.textContent = file.name;
            fileNameContainer.appendChild(fileNameSpan);

            const closeButton = document.createElement('div');
            closeButton.classList.add('w-8', 'h-8', 'cursor-pointer');
            closeButton.innerHTML = `
            <svg viewBox="0 -0.5 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                <g id="SVGRepo_iconCarrier">
                <path d="M6.96967 16.4697C6.67678 16.7626 6.67678 17.2374 6.96967 17.5303C7.26256 17.8232 7.73744 17.8232 8.03033 17.5303L6.96967 16.4697ZM13.0303 12.5303C13.3232 12.2374 13.3232 11.7626 13.0303 11.4697C12.7374 11.1768 12.2626 11.1768 11.9697 11.4697L13.0303 12.5303ZM11.9697 11.4697C11.6768 11.7626 11.6768 12.2374 11.9697 12.5303C12.2626 12.8232 12.7374 12.8232 13.0303 12.5303L11.9697 11.4697ZM18.0303 7.53033C18.3232 7.23744 18.3232 6.76256 18.0303 6.46967C17.7374 6.17678 17.2626 6.17678 16.9697 6.46967L18.0303 7.53033ZM13.0303 11.4697C12.7374 11.1768 12.2626 11.1768 11.9697 11.4697C11.6768 11.7626 11.6768 12.2374 11.9697 12.5303L13.0303 11.4697ZM16.9697 17.5303C17.2626 17.8232 17.7374 17.8232 18.0303 17.5303C18.3232 17.2374 18.3232 16.7626 18.0303 16.4697L16.9697 17.5303ZM11.9697 12.5303C12.2626 12.8232 12.7374 12.8232 13.0303 12.5303C13.3232 12.2374 13.3232 11.7626 13.0303 11.4697L11.9697 12.5303ZM8.03033 6.46967C7.73744 6.17678 7.26256 6.17678 6.96967 6.46967C6.67678 6.76256 6.67678 7.23744 6.96967 7.53033L8.03033 6.46967ZM8.03033 17.5303L13.0303 12.5303L11.9697 11.4697L6.96967 16.4697L8.03033 17.5303ZM13.0303 12.5303L18.0303 7.53033L16.9697 6.46967L11.9697 11.4697L13.0303 12.5303ZM11.9697 12.5303L16.9697 17.5303L18.0303 16.4697L13.0303 11.4697L11.9697 12.5303ZM13.0303 11.4697L8.03033 6.46967L6.96967 7.53033L11.9697 12.5303L13.0303 11.4697Z" fill="#000000"></path>
                </g>
            </svg>
            `;
            fileNameContainer.appendChild(closeButton);

            closeButton.addEventListener('click', () => {
                fileNameContainer.remove();
                // Optionally, if you want to hide the entire container when no files are shown
                if (campaignGalleryTexts.children.length === 0) {
                    campaignGalleryContainer.style.display = "none";
                    campaignGalleryTexts.textContent = 'No file selected';
                }
            });

            campaignGalleryTexts.appendChild(fileNameContainer);
        });
    } else {
        campaignGalleryContainer.style.display = "none"
        campaignGalleryTexts.textContent = 'No file selected';
    }
})

campaignGalleryClose.addEventListener('click', function () {
  campaignGalleryInput.value = "";
  campaignGalleryContainer.style.display = "none";
  campaignGalleryTexts.textContent = 'No file selected';
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