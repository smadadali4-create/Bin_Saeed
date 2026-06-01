document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('three-canvas');
    if (!canvas) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a0f);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 16;

    const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: true,
        alpha: true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;

    const ambientLight = new THREE.AmbientLight(0x404060);
    scene.add(ambientLight);

    const mainLight = new THREE.DirectionalLight(0xD4AF37, 1.5);
    mainLight.position.set(5, 5, 5);
    scene.add(mainLight);

    const fillLight = new THREE.DirectionalLight(0x8B5CF6, 0.5);
    fillLight.position.set(-5, 3, -3);
    scene.add(fillLight);

    const pointLight = new THREE.PointLight(0xD4AF37, 0.8, 30);
    pointLight.position.set(-5, 3, 5);
    scene.add(pointLight);

    const shapes = [];

    function createGoldMaterial(color, emissiveIntensity, opacity, wireframe) {
        return new THREE.MeshPhongMaterial({
            color: color,
            emissive: color,
            emissiveIntensity: emissiveIntensity || 0.1,
            wireframe: wireframe || false,
            transparent: true,
            opacity: opacity || 0.8,
            shininess: 100,
            metalness: 0.3,
        });
    }

    const goldMat = createGoldMaterial(0xD4AF37, 0.15, 0.85);
    const goldLightMat = createGoldMaterial(0xF0D060, 0.12, 0.75);
    const purpleMat = createGoldMaterial(0x8B5CF6, 0.1, 0.6);
    const wireMat = createGoldMaterial(0xD4AF37, 0.05, 0.25, true);

    const geo1 = new THREE.IcosahedronGeometry(1.4, 0);
    const mesh1 = new THREE.Mesh(geo1, goldMat);
    mesh1.position.set(-3.5, 1.5, -2);
    scene.add(mesh1);
    shapes.push(mesh1);

    const geo2 = new THREE.TorusKnotGeometry(0.9, 0.35, 100, 16);
    const mesh2 = new THREE.Mesh(geo2, goldLightMat);
    mesh2.position.set(4, -1, -1);
    scene.add(mesh2);
    shapes.push(mesh2);

    const geo3 = new THREE.OctahedronGeometry(1.2);
    const mesh3 = new THREE.Mesh(geo3, wireMat);
    mesh3.position.set(0, -2.5, -5);
    scene.add(mesh3);
    shapes.push(mesh3);

    const geo4 = new THREE.TorusGeometry(0.9, 0.35, 20, 60);
    const mesh4 = new THREE.Mesh(geo4, purpleMat);
    mesh4.position.set(-3, -1.8, 0.5);
    scene.add(mesh4);
    shapes.push(mesh4);

    const geo5 = new THREE.DodecahedronGeometry(0.8);
    const mesh5 = new THREE.Mesh(geo5, createGoldMaterial(0xF0D060, 0.1, 0.5));
    mesh5.position.set(3.5, 2, -3);
    scene.add(mesh5);
    shapes.push(mesh5);

    const geo6 = new THREE.ConeGeometry(0.8, 1.6, 6);
    const mesh6 = new THREE.Mesh(geo6, createGoldMaterial(0xD4AF37, 0.08, 0.4));
    mesh6.position.set(-1, -0.5, -6);
    scene.add(mesh6);
    shapes.push(mesh6);

    const particleCount = 2000;
    const particleGeometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 60;
        positions[i + 1] = (Math.random() - 0.5) * 40;
        positions[i + 2] = (Math.random() - 0.5) * 40 - 10;

        const colorChoice = Math.random();
        if (colorChoice < 0.4) {
            colors[i] = 0.83; colors[i + 1] = 0.69; colors[i + 2] = 0.22;
        } else if (colorChoice < 0.7) {
            colors[i] = 0.55; colors[i + 1] = 0.36; colors[i + 2] = 0.96;
        } else {
            colors[i] = 1.0; colors[i + 1] = 1.0; colors[i + 2] = 1.0;
        }
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMaterial = new THREE.PointsMaterial({
        size: 0.1,
        vertexColors: true,
        transparent: true,
        opacity: 0.7,
        blending: THREE.AdditiveBlending,
        sizeAttenuation: true,
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    const ringParticles = 500;
    const ringGeo = new THREE.BufferGeometry();
    const ringPos = new Float32Array(ringParticles * 3);
    for (let i = 0; i < ringParticles; i++) {
        const angle = (i / ringParticles) * Math.PI * 2;
        const radius = 4 + Math.random() * 2;
        ringPos[i * 3] = Math.cos(angle) * radius;
        ringPos[i * 3 + 1] = (Math.random() - 0.5) * 0.5;
        ringPos[i * 3 + 2] = Math.sin(angle) * radius - 2;
    }
    ringGeo.setAttribute('position', new THREE.BufferAttribute(ringPos, 3));
    const ringMat = new THREE.PointsMaterial({
        color: 0xD4AF37,
        size: 0.06,
        transparent: true,
        opacity: 0.4,
        blending: THREE.AdditiveBlending,
    });
    const ring = new THREE.Points(ringGeo, ringMat);
    scene.add(ring);

    const clock = new THREE.Clock();

    let mouseX = 0;
    let mouseY = 0;
    document.addEventListener('mousemove', function(e) {
        mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
        mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    });

    function animate() {
        const elapsed = clock.getElapsedTime();

        mesh1.rotation.x = elapsed * 0.3;
        mesh1.rotation.y = elapsed * 0.5;
        mesh1.position.y = 1.5 + Math.sin(elapsed * 0.5) * 0.6;

        mesh2.rotation.x = elapsed * 0.4;
        mesh2.rotation.y = elapsed * 0.3;
        mesh2.position.y = -1 + Math.sin(elapsed * 0.7 + 1) * 0.6;

        mesh3.rotation.x = elapsed * 0.2;
        mesh3.rotation.y = elapsed * 0.4;
        mesh3.position.y = -2.5 + Math.sin(elapsed * 0.3 + 2) * 0.5;

        mesh4.rotation.x = elapsed * 0.5;
        mesh4.rotation.y = elapsed * 0.6;
        mesh4.position.y = -1.8 + Math.sin(elapsed * 0.6 + 3) * 0.6;

        mesh5.rotation.x = elapsed * 0.35;
        mesh5.rotation.y = elapsed * 0.45;
        mesh5.position.y = 2 + Math.sin(elapsed * 0.55 + 4) * 0.5;

        mesh6.rotation.x = elapsed * 0.25;
        mesh6.rotation.y = elapsed * 0.55;
        mesh6.position.y = -0.5 + Math.sin(elapsed * 0.4 + 5) * 0.7;

        const goldHue = 45 + Math.sin(elapsed * 0.2) * 10;
        const goldColor = new THREE.Color(`hsl(${goldHue}, 100%, 55%)`);
        goldMat.color.copy(goldColor);
        goldMat.emissive.copy(goldColor);
        goldMat.emissiveIntensity = 0.15 + Math.sin(elapsed * 0.5) * 0.05;

        const goldLightHue = 50 + Math.sin(elapsed * 0.25 + 1) * 8;
        const goldLightColor = new THREE.Color(`hsl(${goldLightHue}, 100%, 60%)`);
        goldLightMat.color.copy(goldLightColor);
        goldLightMat.emissive.copy(goldLightColor);

        const purpleHue = 260 + Math.sin(elapsed * 0.3) * 20;
        const purpleColor = new THREE.Color(`hsl(${purpleHue}, 90%, 55%)`);
        purpleMat.color.copy(purpleColor);
        purpleMat.emissive.copy(purpleColor);

        goldMat.opacity = 0.75 + Math.sin(elapsed * 0.3) * 0.1;
        goldLightMat.opacity = 0.65 + Math.sin(elapsed * 0.4 + 0.5) * 0.1;

        particles.rotation.y = elapsed * 0.015;
        particles.rotation.x = Math.sin(elapsed * 0.005) * 0.1;

        ring.rotation.y = elapsed * 0.2;
        ring.rotation.x = Math.sin(elapsed * 0.1) * 0.1;

        camera.position.x += (mouseX * 3 - camera.position.x) * 0.02;
        camera.position.y += (-mouseY * 2 - camera.position.y) * 0.02;
        camera.lookAt(0, 0, -3);

        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    }

    animate();

    window.addEventListener('resize', function() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });
});
