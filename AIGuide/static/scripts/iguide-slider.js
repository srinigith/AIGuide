function iguideslider(sliderid, apipath) {
	const slider = document.getElementById(sliderid);//document.querySelector('.iguide-slider');
	//const slides = slider.querySelectorAll('.slide');
	let currentSlide = 0;

	fetch(apipath)
		.then(response => response.json())
		.then(data => {
			console.log("Image data", data);
			idx = 0;
			data.images_results.forEach((image, index) => {				
				console.log("Image", image);
				const slide = document.createElement('div');//slides[index];
				slide.classList.add('slide');
				if (idx === 0) {
					slide.style.display = 'block';
				}
				idx++;
				const img = document.createElement('img');
				img.src = image.original;
				//img.alt = image.caption;
				slide.appendChild(img);
				slider.appendChild(slide);
			});

			function nextSlide() {
				const slides = slider.querySelectorAll('.slide');
				slides[currentSlide].style.display = 'none';
				currentSlide = (currentSlide + 1) % slides.length;
				slides[currentSlide].style.display = 'block';
			}

			function prevSlide() {
				const slides = slider.querySelectorAll('.slide');
				slides[currentSlide].style.display = 'none';
				currentSlide = (currentSlide - 1 + slides.length) % slides.length;
				slides[currentSlide].style.display = 'block';
			}



			// Add event listeners for next and previous buttons
			const nextBtn = document.createElement('button');
			nextBtn.textContent = 'Next';
			nextBtn.addEventListener('click', nextSlide);
			slider.appendChild(nextBtn);

			const prevBtn = document.createElement('button');
			prevBtn.textContent = 'Previous';
			prevBtn.addEventListener('click', prevSlide);
			slider.appendChild(prevBtn);
		});
}
