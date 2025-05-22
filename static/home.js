// Header scroll effect
const header = document.querySelector('header');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// Three.js setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
const container = document.querySelector('.canvas-container');

renderer.setSize(window.innerWidth, window.innerHeight);
container.appendChild(renderer.domElement);

// Create particles
const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 2000;
const posArray = new Float32Array(particlesCount * 3);

for (let i = 0; i < particlesCount * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 5;
}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

// Material
const particlesMaterial = new THREE.PointsMaterial({
    size: 0.005,
    color: '#8E7566',
    transparent: true,
    opacity: 0.8,
});

// Mesh
const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);

// Create flying papers
const papers = [];
const paperCount = 15;

// Paper texture
const paperTexture = new THREE.TextureLoader().load('/static/paper-texture.png');
paperTexture.wrapS = THREE.RepeatWrapping;
paperTexture.wrapT = THREE.RepeatWrapping;

for (let i = 0; i < paperCount; i++) {
    // Create paper geometry
    const paperGeometry = new THREE.PlaneGeometry(0.2, 0.3);
    const paperMaterial = new THREE.MeshBasicMaterial({
        color: '#F5F1EB',
        transparent: true,
        opacity: 0.8,
        side: THREE.DoubleSide,
        map: paperTexture
    });

    const paper = new THREE.Mesh(paperGeometry, paperMaterial);
    
    // Random position
    paper.position.x = (Math.random() - 0.5) * 5;
    paper.position.y = (Math.random() - 0.5) * 5;
    paper.position.z = (Math.random() - 0.5) * 2;
    
    // Random rotation
    paper.rotation.x = Math.random() * Math.PI;
    paper.rotation.y = Math.random() * Math.PI;
    paper.rotation.z = Math.random() * Math.PI;
    
    // Add velocity and rotation speed
    paper.userData = {
        velocity: new THREE.Vector3(
            (Math.random() - 0.5) * 0.001,
            (Math.random() - 0.5) * 0.001,
            (Math.random() - 0.5) * 0.001
        ),
        rotationSpeed: new THREE.Vector3(
            (Math.random() - 0.5) * 0.001,
            (Math.random() - 0.5) * 0.001,
            (Math.random() - 0.5) * 0.001
        )
    };
    
    papers.push(paper);
    scene.add(paper);
}

// Camera position
camera.position.z = 2;

// Mouse movement effect
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (event) => {
    mouseX = event.clientX / window.innerWidth - 0.5;
    mouseY = event.clientY / window.innerHeight - 0.5;
});

// Animation
const animate = () => {
    requestAnimationFrame(animate);

    // Update particles
    particlesMesh.rotation.x += 0.0005;
    particlesMesh.rotation.y += 0.0005;

    // Smooth mouse movement for particles
    particlesMesh.rotation.x += (mouseY * 0.5 - particlesMesh.rotation.x) * 0.05;
    particlesMesh.rotation.y += (mouseX * 0.5 - particlesMesh.rotation.y) * 0.05;

    // Update papers
    papers.forEach(paper => {
        // Update position
        paper.position.add(paper.userData.velocity);
        
        // Update rotation
        paper.rotation.x += paper.userData.rotationSpeed.x;
        paper.rotation.y += paper.userData.rotationSpeed.y;
        paper.rotation.z += paper.userData.rotationSpeed.z;
        
        // Add slight mouse influence
        paper.position.x += mouseX * 0.0001;
        paper.position.y += mouseY * 0.0001;
        
        // Boundary check and reset
        if (Math.abs(paper.position.x) > 3) {
            paper.position.x = -paper.position.x * 0.9;
        }
        if (Math.abs(paper.position.y) > 3) {
            paper.position.y = -paper.position.y * 0.9;
        }
        if (Math.abs(paper.position.z) > 2) {
            paper.position.z = -paper.position.z * 0.9;
        }
    });

    renderer.render(scene, camera);
};

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Start animation
animate();
