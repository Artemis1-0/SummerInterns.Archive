let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

gsap.registerPlugin(ScrollTrigger);


const panels = gsap.utils.toArray(".panel")
let tl = gsap.timeline({paused: true})
tl.to("#text-svg", {scale: 100, xPercent: -300 ,  transformOrigin: "50% 50%"})
.to("#text-svg", {scale: "+=30", xPercent: "-=110"  })

panels.forEach(panel => {
  ScrollTrigger.create({
    trigger: panel,
    start: "top top",
    end: "90% 30%",
    scrub: 1,
    pin: true,

    animation: tl.play()
  })
})