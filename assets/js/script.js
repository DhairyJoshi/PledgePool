const wrapper = document.querySelector('#wrapper');
const carousel = document.querySelector('#image-carousel');
const images = document.querySelectorAll('.myimages');
const indicators = document.querySelectorAll('.indicator-dot');
const pageIndicator = document.querySelector('#page-indicator');

images.forEach((slide, index) => {
    slide.style.left = `${index * 100}%`;
});

let counter = 0;

const slideImage = () => {
    images.forEach((e) => {
        e.style.transform = `translateX(-${counter * 100}%)`;
    });
    
    indicators.forEach((dot, index) => {
        dot.style.backgroundColor = index === counter ? 'white' : '#ffffff66';
    });
    
    pageIndicator.textContent = `Page: ${counter + 1}/${images.length}`;
};

// Function to validate inputs on the current slide
const validateInputs = () => {
    const currentSlide = images[counter];
    const requiredInputs = currentSlide.querySelectorAll('input[required]');
    let allFilled = true;

    requiredInputs.forEach((input) => {
        if (!input.value) {
            allFilled = false;
        }
    });

    return allFilled;
};

const prevSlide = () => {
    if (counter > 0) {
        counter--;
        slideImage();
    }
};

const nextSlide = () => {
    // Validate inputs before moving to the next slide
    if (validateInputs()) {
        if (counter < images.length - 1) {
            counter++;
            slideImage();
        }
    }
};

indicators.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        counter = index;
        slideImage(); 
    });
});