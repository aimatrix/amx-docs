---
title: AIMatrix - Enter the Business Matrix
description: Step into a parallel digital universe where AI agents simulate, optimize, and transform your business reality
keywords: AI simulation, business matrix, digital twin, AI agents, virtual business world, autonomous systems, predictive simulation, business transformation
layout: hextra-home
toc: false
---

<style>
/* Clean, modern design system */
:root {
  --matrix-green: #00ff00;
  --matrix-dark-green: #00cc00;
  --matrix-bg: #0a0a0a;
  --matrix-card: rgba(0, 20, 0, 0.6);
  --text-primary: #ffffff;
  --text-secondary: #b0b0b0;
}

* {
  box-sizing: border-box;
}

/* Container system for proper alignment - centered */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Hero Section with 3D Avatar */
.hero-section {
  background: linear-gradient(180deg, #000000 0%, #0a1a0a 100%);
  padding: 80px 20px;
  position: relative;
  overflow: hidden;
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Matrix rain effect */
.matrix-rain {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.1;
  pointer-events: none;
}

/* 3D Avatar Container - Bigger and centered */
#robot-container {
  position: absolute;
  right: 50px;
  top: 50%;
  transform: translateY(-50%);
  width: 600px;
  height: 600px;
  z-index: 10;
}

@media (max-width: 1200px) {
  #robot-container {
    width: 400px;
    height: 400px;
    right: 20px;
  }
}

/* Hero Content - Better alignment */
.hero-content {
  position: relative;
  z-index: 20;
  max-width: 600px;
  width: 100%;
  padding-right: 650px;
}

@media (max-width: 1200px) {
  .hero-content {
    padding-right: 450px;
  }
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #ffffff 0%, #00ff00 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: clamp(1.2rem, 2vw, 1.5rem);
  color: var(--text-secondary);
  margin-bottom: 30px;
  line-height: 1.5;
}

.hero-description {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 40px;
  line-height: 1.6;
}

/* Buttons */
.btn-group {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.btn-primary {
  padding: 15px 35px;
  background: linear-gradient(135deg, var(--matrix-green), var(--matrix-dark-green));
  color: #000;
  text-decoration: none;
  border-radius: 30px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  display: inline-block;
  box-shadow: 0 4px 15px rgba(0, 255, 0, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 255, 0, 0.5);
}

.btn-secondary {
  padding: 15px 35px;
  background: transparent;
  color: var(--matrix-green);
  text-decoration: none;
  border: 2px solid var(--matrix-green);
  border-radius: 30px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  display: inline-block;
}

.btn-secondary:hover {
  background: rgba(0, 255, 0, 0.1);
  transform: translateY(-2px);
}

/* Section Styles - Centered content */
.section {
  padding: 80px 20px;
  position: relative;
  display: flex;
  justify-content: center;
}

.section-dark {
  background: var(--matrix-bg);
}

.section-title {
  font-size: clamp(2rem, 4vw, 3rem);
  text-align: center;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.section-subtitle {
  font-size: 1.2rem;
  text-align: center;
  color: var(--text-secondary);
  margin-bottom: 60px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* Grid System - Centered */
.grid {
  display: grid;
  gap: 30px;
  margin: 0 auto 40px;
  width: 100%;
  max-width: 1200px;
}

.grid-2 {
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.grid-3 {
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

.grid-4 {
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

/* Cards */
.card {
  background: var(--matrix-card);
  border: 1px solid rgba(0, 255, 0, 0.2);
  border-radius: 12px;
  padding: 30px;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  border-color: var(--matrix-green);
  box-shadow: 0 10px 30px rgba(0, 255, 0, 0.2);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 20px;
  display: block;
}

.card-title {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: var(--text-primary);
}

.card-text {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Feature Box - Centered */
.feature-box {
  background: linear-gradient(135deg, rgba(0, 255, 0, 0.1) 0%, transparent 100%);
  border-left: 4px solid var(--matrix-green);
  padding: 20px;
  margin: 20px auto;
  border-radius: 0 8px 8px 0;
  max-width: 800px;
}

/* Stats - Centered horizontal layout */
.stat-grid {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 40px auto;
  flex-wrap: wrap;
  max-width: 1200px;
  width: 100%;
}

@media (min-width: 768px) {
  .stat-grid {
    flex-wrap: nowrap;
  }
}

.stat-card {
  flex: 1;
  min-width: 150px;
  text-align: center;
  padding: 30px 20px;
  background: rgba(0, 255, 0, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(0, 255, 0, 0.2);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  background: rgba(0, 255, 0, 0.1);
  box-shadow: 0 10px 30px rgba(0, 255, 0, 0.2);
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: var(--matrix-green);
  display: block;
  margin-bottom: 10px;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  #robot-container {
    position: static;
    transform: none;
    width: 300px;
    height: 300px;
    margin: 20px auto;
  }
  
  .hero-content {
    max-width: 100%;
    text-align: center;
    padding-right: 0;
  }
  
  .btn-group {
    justify-content: center;
  }
  
  .grid {
    grid-template-columns: 1fr;
  }
}

/* Matrix Digital Rain Canvas */
#matrix-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  opacity: 0.1;
}
</style>

<!-- Hero Section with 3D Robot -->
<div class="hero-section">
  <canvas id="matrix-canvas"></canvas>
  
  <div class="container">
    <div class="hero-content">
      <h1 class="hero-title">Enter the Business Matrix</h1>
      <p class="hero-subtitle">Where Reality Meets Infinite Possibility</p>
      <p class="hero-description">
        Step into a parallel digital universe where AI agents don't just automate—they simulate, predict, and reshape your business reality. Like entering the Matrix, see your business from a dimension where every possibility can be explored, tested, and optimized before affecting the real world.
      </p>
      <div class="btn-group">
        <a href="/demo" class="btn-primary">Enter the Matrix</a>
        <a href="#vision" class="btn-secondary">Explore the Vision</a>
      </div>
    </div>
  </div>
  
  <!-- 3D Human Avatar Container -->
  <div id="robot-container">
    <canvas id="robot-canvas"></canvas>
    <div id="loading-spinner" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #00ff00; font-size: 1.2em;">Loading AI Avatar...</div>
  </div>
</div>

<!-- Vision Section -->
<section id="vision" class="section">
  <div class="container">
    <h2 class="section-title">The Dawn of Business AI</h2>
    <p class="section-subtitle">
      We're at the beginning of an unprecedented transformation. AIMatrix isn't just another tool—it's a gateway to a new dimension of business operation.
    </p>
    
    <div class="grid grid-3">
      <div class="card">
        <span class="card-icon">🌌</span>
        <h3 class="card-title">Parallel Simulation</h3>
        <p class="card-text">Run thousands of business scenarios simultaneously in a virtual environment before committing to real-world changes.</p>
      </div>
      
      <div class="card">
        <span class="card-icon">🔮</span>
        <h3 class="card-title">Predictive Reality</h3>
        <p class="card-text">AI agents that see patterns invisible to humans, predicting outcomes with quantum-like probability calculations.</p>
      </div>
      
      <div class="card">
        <span class="card-icon">♾️</span>
        <h3 class="card-title">Infinite Optimization</h3>
        <p class="card-text">Continuously evolving systems that learn, adapt, and optimize without human intervention.</p>
      </div>
    </div>
  </div>
</section>

<!-- Matrix Capabilities -->
<section class="section section-dark">
  <div class="container">
    <h2 class="section-title">Your Business, Reimagined</h2>
    <p class="section-subtitle">What becomes possible when you operate in multiple dimensions?</p>
    
    <div class="grid grid-2">
      <div class="feature-box">
        <h3>🤖 Autonomous Agents</h3>
        <p>Deploy thousands of AI agents that work 24/7, learning from each interaction and sharing knowledge instantly across your entire digital ecosystem.</p>
      </div>
      
      <div class="feature-box">
        <h3>⚡ Quantum Decision Making</h3>
        <p>Evaluate millions of possibilities in seconds, choosing optimal paths through complex business landscapes.</p>
      </div>
      
      <div class="feature-box">
        <h3>🧬 Self-Evolving Systems</h3>
        <p>Business processes that rewrite themselves, continuously improving without human intervention.</p>
      </div>
      
      <div class="feature-box">
        <h3>🌐 Reality Bridge</h3>
        <p>Seamlessly connect your virtual simulations to real-world systems, implementing tested strategies instantly.</p>
      </div>
    </div>
  </div>
</section>

<!-- Performance Metrics -->
<section class="section">
  <div class="container">
    <h2 class="section-title">Beyond Human Limits</h2>
    
    <div class="stat-grid">
      <div class="stat-card">
        <span class="stat-number">∞</span>
        <span class="stat-label">Parallel Simulations</span>
      </div>
      <div class="stat-card">
        <span class="stat-number">1ms</span>
        <span class="stat-label">Decision Latency</span>
      </div>
      <div class="stat-card">
        <span class="stat-number">24/7</span>
        <span class="stat-label">Autonomous Operation</span>
      </div>
      <div class="stat-card">
        <span class="stat-number">10^6</span>
        <span class="stat-label">Scenarios per Second</span>
      </div>
    </div>
  </div>
</section>

<!-- Use Cases -->
<section class="section section-dark">
  <div class="container">
    <h2 class="section-title">Reality Transformation</h2>
    <p class="section-subtitle">See how businesses are already living in the future</p>
    
    <div class="grid grid-3">
      <div class="card">
        <h3 class="card-title">Supply Chain Oracle</h3>
        <p class="card-text">Predict disruptions 30 days before they happen. Automatically reroute, reorder, and optimize without human intervention.</p>
        <p style="color: var(--matrix-green); margin-top: 15px;">↗ 99.9% availability achieved</p>
      </div>
      
      <div class="card">
        <h3 class="card-title">Customer Mind Reading</h3>
        <p class="card-text">AI that knows what customers want before they do, personalizing experiences at a quantum level.</p>
        <p style="color: var(--matrix-green); margin-top: 15px;">↗ 5x conversion rate</p>
      </div>
      
      <div class="card">
        <h3 class="card-title">Financial Time Travel</h3>
        <p class="card-text">See your financial future across thousands of market scenarios, optimizing for any possible outcome.</p>
        <p style="color: var(--matrix-green); margin-top: 15px;">↗ 40% risk reduction</p>
      </div>
    </div>
  </div>
</section>

<!-- Technology Stack -->
<section class="section">
  <div class="container">
    <h2 class="section-title">The Architecture of Tomorrow</h2>
    
    <div class="grid grid-4">
      <div class="card">
        <span class="card-icon">🧠</span>
        <h4 class="card-title">Neural Orchestration</h4>
        <p class="card-text">Multi-model AI coordination</p>
      </div>
      
      <div class="card">
        <span class="card-icon">⚛️</span>
        <h4 class="card-title">Quantum Logic</h4>
        <p class="card-text">Probability-based decisions</p>
      </div>
      
      <div class="card">
        <span class="card-icon">🔄</span>
        <h4 class="card-title">Self-Learning</h4>
        <p class="card-text">Continuous evolution</p>
      </div>
      
      <div class="card">
        <span class="card-icon">🌊</span>
        <h4 class="card-title">Reality Synthesis</h4>
        <p class="card-text">Virtual-physical bridge</p>
      </div>
    </div>
  </div>
</section>

<!-- CTA Section -->
<section class="section section-dark" style="text-align: center; padding: 100px 20px;">
  <div class="container">
    <h2 class="section-title">Ready to Transcend Reality?</h2>
    <p class="section-subtitle" style="margin-bottom: 40px;">
      The future isn't coming—it's here. Join the businesses already operating in the next dimension.
    </p>
    <div class="btn-group" style="justify-content: center;">
      <a href="/demo" class="btn-primary">Experience the Matrix</a>
      <a href="/contact" class="btn-secondary">Talk to an Agent</a>
    </div>
  </div>
</section>

<!-- JavaScript for Matrix Rain and 3D Robot -->
<script>
// Matrix Digital Rain Effect
(function() {
  const canvas = document.getElementById('matrix-canvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  const characters = 'アイマトリックス0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const fontSize = 14;
  const columns = canvas.width / fontSize;
  const drops = Array(Math.floor(columns)).fill(1);
  
  function draw() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#00ff00';
    ctx.font = fontSize + 'px monospace';
    
    for (let i = 0; i < drops.length; i++) {
      const text = characters[Math.floor(Math.random() * characters.length)];
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);
      
      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }
      drops[i]++;
    }
  }
  
  setInterval(draw, 33);
  
  window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  });
})();

// Load Babylon.js and create human avatar
(function() {
  // First load Babylon.js
  const babylonScript = document.createElement('script');
  babylonScript.src = 'https://cdn.babylonjs.com/babylon.js';
  babylonScript.onload = function() {
    // Then load Babylon loaders for 3D models
    const loadersScript = document.createElement('script');
    loadersScript.src = 'https://cdn.babylonjs.com/loaders/babylonjs.loaders.min.js';
    loadersScript.onload = initBabylon3DAvatar;
    document.head.appendChild(loadersScript);
  };
  document.head.appendChild(babylonScript);
  
  function initBabylon3DAvatar() {
    const canvas = document.getElementById('robot-canvas');
    const container = document.getElementById('robot-container');
    if (!canvas || !container) return;
    
    // Create Babylon.js engine
    const engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
    
    // Create scene
    const scene = new BABYLON.Scene(engine);
    scene.clearColor = new BABYLON.Color4(0, 0, 0, 0);
    
    // Create camera - closer view for avatar
    const camera = new BABYLON.ArcRotateCamera('camera', -Math.PI / 2, Math.PI / 2, 3, new BABYLON.Vector3(0, 1, 0), scene);
    camera.attachControl(canvas, false);
    camera.lowerRadiusLimit = 2;
    camera.upperRadiusLimit = 5;
    camera.panningSensibility = 0; // Disable panning
    
    // Create lights for avatar
    const light1 = new BABYLON.HemisphericLight('light1', new BABYLON.Vector3(0, 1, 0), scene);
    light1.intensity = 0.8;
    
    const light2 = new BABYLON.DirectionalLight('light2', new BABYLON.Vector3(-1, -2, -1), scene);
    light2.position = new BABYLON.Vector3(3, 3, 3);
    light2.intensity = 0.5;
    
    const light3 = new BABYLON.PointLight('light3', new BABYLON.Vector3(1, 2, 2), scene);
    light3.intensity = 0.3;
    light3.diffuse = new BABYLON.Color3(0.2, 1, 0.2);
    
    // Hide loading spinner after scene is ready
    scene.executeWhenReady(() => {
      const spinner = document.getElementById('loading-spinner');
      if (spinner) spinner.style.display = 'none';
    });
    
    // Create materials for human avatar
    const skinMaterial = new BABYLON.StandardMaterial('skinMat', scene);
    skinMaterial.diffuseColor = new BABYLON.Color3(0.95, 0.8, 0.7);
    skinMaterial.specularColor = new BABYLON.Color3(0.2, 0.2, 0.2);
    skinMaterial.emissiveColor = new BABYLON.Color3(0.05, 0.02, 0.01);
    
    const suitMaterial = new BABYLON.StandardMaterial('suitMat', scene);
    suitMaterial.diffuseColor = new BABYLON.Color3(0.1, 0.1, 0.15);
    suitMaterial.specularColor = new BABYLON.Color3(0.3, 0.3, 0.3);
    suitMaterial.emissiveColor = new BABYLON.Color3(0, 0.1, 0);
    
    const eyeMaterial = new BABYLON.StandardMaterial('eyeMat', scene);
    eyeMaterial.diffuseColor = new BABYLON.Color3(1, 1, 1);
    eyeMaterial.emissiveColor = new BABYLON.Color3(0.1, 0.1, 0.1);
    
    const irisMaterial = new BABYLON.StandardMaterial('irisMat', scene);
    irisMaterial.diffuseColor = new BABYLON.Color3(0, 0.5, 0.2);
    irisMaterial.emissiveColor = new BABYLON.Color3(0, 0.3, 0);
    
    const glowMaterial = new BABYLON.StandardMaterial('glowMat', scene);
    glowMaterial.emissiveColor = new BABYLON.Color3(0, 1, 0);
    glowMaterial.diffuseColor = new BABYLON.Color3(0, 1, 0);
    
    // Create human avatar parts
    // Head - more realistic proportions
    const head = BABYLON.MeshBuilder.CreateSphere('head', {diameter: 0.5, segments: 32}, scene);
    head.position.y = 1.7;
    head.scaling.y = 1.1;
    head.material = skinMaterial;
    
    // Face features
    // Eyes
    const leftEyeWhite = BABYLON.MeshBuilder.CreateSphere('leftEyeWhite', {diameter: 0.08, segments: 16}, scene);
    leftEyeWhite.position = new BABYLON.Vector3(-0.1, 1.72, 0.22);
    leftEyeWhite.material = eyeMaterial;
    
    const rightEyeWhite = BABYLON.MeshBuilder.CreateSphere('rightEyeWhite', {diameter: 0.08, segments: 16}, scene);
    rightEyeWhite.position = new BABYLON.Vector3(0.1, 1.72, 0.22);
    rightEyeWhite.material = eyeMaterial;
    
    // Irises
    const leftIris = BABYLON.MeshBuilder.CreateSphere('leftIris', {diameter: 0.05, segments: 8}, scene);
    leftIris.position = new BABYLON.Vector3(-0.1, 1.72, 0.25);
    leftIris.material = irisMaterial;
    
    const rightIris = BABYLON.MeshBuilder.CreateSphere('rightIris', {diameter: 0.05, segments: 8}, scene);
    rightIris.position = new BABYLON.Vector3(0.1, 1.72, 0.25);
    rightIris.material = irisMaterial;
    
    // Pupils
    const pupilMat = new BABYLON.StandardMaterial('pupilMat', scene);
    pupilMat.diffuseColor = new BABYLON.Color3(0, 0, 0);
    
    const leftPupil = BABYLON.MeshBuilder.CreateSphere('leftPupil', {diameter: 0.02, segments: 8}, scene);
    leftPupil.position = new BABYLON.Vector3(-0.1, 1.72, 0.27);
    leftPupil.material = pupilMat;
    
    const rightPupil = BABYLON.MeshBuilder.CreateSphere('rightPupil', {diameter: 0.02, segments: 8}, scene);
    rightPupil.position = new BABYLON.Vector3(0.1, 1.72, 0.27);
    rightPupil.material = pupilMat;
    
    // Nose (simple representation)
    const nose = BABYLON.MeshBuilder.CreateBox('nose', {width: 0.04, height: 0.06, depth: 0.05}, scene);
    nose.position = new BABYLON.Vector3(0, 1.65, 0.24);
    nose.material = skinMaterial;
    
    // Mouth
    const mouth = BABYLON.MeshBuilder.CreateTorus('mouth', {diameter: 0.1, thickness: 0.01, tessellation: 16}, scene);
    mouth.position = new BABYLON.Vector3(0, 1.55, 0.22);
    mouth.rotation.x = Math.PI / 2;
    mouth.scaling = new BABYLON.Vector3(1, 0.5, 1);
    const mouthMat = new BABYLON.StandardMaterial('mouthMat', scene);
    mouthMat.diffuseColor = new BABYLON.Color3(0.6, 0.3, 0.3);
    mouth.material = mouthMat;
    
    // Hair
    const hair = BABYLON.MeshBuilder.CreateSphere('hair', {diameter: 0.52, segments: 16}, scene);
    hair.position.y = 1.75;
    hair.scaling.y = 0.7;
    const hairMat = new BABYLON.StandardMaterial('hairMat', scene);
    hairMat.diffuseColor = new BABYLON.Color3(0.1, 0.1, 0.1);
    hairMat.specularColor = new BABYLON.Color3(0.2, 0.2, 0.2);
    hair.material = hairMat;
    
    // Neck
    const neck = BABYLON.MeshBuilder.CreateCylinder('neck', {height: 0.2, diameter: 0.15}, scene);
    neck.position.y = 1.35;
    neck.material = skinMaterial;
    
    // Body (torso) - business suit style
    const torso = BABYLON.MeshBuilder.CreateBox('torso', {height: 0.8, width: 0.5, depth: 0.25}, scene);
    torso.position.y = 0.8;
    torso.material = suitMaterial;
    
    // Shoulders
    const leftShoulder = BABYLON.MeshBuilder.CreateSphere('leftShoulder', {diameter: 0.15}, scene);
    leftShoulder.position = new BABYLON.Vector3(-0.3, 1.15, 0);
    leftShoulder.material = suitMaterial;
    
    const rightShoulder = BABYLON.MeshBuilder.CreateSphere('rightShoulder', {diameter: 0.15}, scene);
    rightShoulder.position = new BABYLON.Vector3(0.3, 1.15, 0);
    rightShoulder.material = suitMaterial;
    
    // Arms
    const leftUpperArm = BABYLON.MeshBuilder.CreateCylinder('leftUpperArm', {height: 0.4, diameter: 0.1}, scene);
    leftUpperArm.position = new BABYLON.Vector3(-0.3, 0.9, 0);
    leftUpperArm.material = suitMaterial;
    
    const rightUpperArm = BABYLON.MeshBuilder.CreateCylinder('rightUpperArm', {height: 0.4, diameter: 0.1}, scene);
    rightUpperArm.position = new BABYLON.Vector3(0.3, 0.9, 0);
    rightUpperArm.material = suitMaterial;
    
    const leftLowerArm = BABYLON.MeshBuilder.CreateCylinder('leftLowerArm', {height: 0.4, diameter: 0.08}, scene);
    leftLowerArm.position = new BABYLON.Vector3(-0.3, 0.5, 0);
    leftLowerArm.material = skinMaterial;
    
    const rightLowerArm = BABYLON.MeshBuilder.CreateCylinder('rightLowerArm', {height: 0.4, diameter: 0.08}, scene);
    rightLowerArm.position = new BABYLON.Vector3(0.3, 0.5, 0);
    rightLowerArm.rotation.z = -0.2;
    rightLowerArm.material = skinMaterial;
    
    // Hands
    const leftHand = BABYLON.MeshBuilder.CreateSphere('leftHand', {diameter: 0.08}, scene);
    leftHand.position = new BABYLON.Vector3(-0.3, 0.25, 0);
    leftHand.material = skinMaterial;
    
    const rightHand = BABYLON.MeshBuilder.CreateSphere('rightHand', {diameter: 0.08}, scene);
    rightHand.position = new BABYLON.Vector3(0.32, 0.28, 0.05);
    rightHand.material = skinMaterial;
    
    // Waist/Belt area
    const waist = BABYLON.MeshBuilder.CreateCylinder('waist', {height: 0.1, diameter: 0.35}, scene);
    waist.position.y = 0.35;
    const beltMat = new BABYLON.StandardMaterial('beltMat', scene);
    beltMat.diffuseColor = new BABYLON.Color3(0.05, 0.05, 0.05);
    waist.material = beltMat;
    
    // Legs
    const leftUpperLeg = BABYLON.MeshBuilder.CreateCylinder('leftUpperLeg', {height: 0.5, diameter: 0.12}, scene);
    leftUpperLeg.position = new BABYLON.Vector3(-0.12, 0, 0);
    leftUpperLeg.material = suitMaterial;
    
    const rightUpperLeg = BABYLON.MeshBuilder.CreateCylinder('rightUpperLeg', {height: 0.5, diameter: 0.12}, scene);
    rightUpperLeg.position = new BABYLON.Vector3(0.12, 0, 0);
    rightUpperLeg.material = suitMaterial;
    
    const leftLowerLeg = BABYLON.MeshBuilder.CreateCylinder('leftLowerLeg', {height: 0.5, diameter: 0.1}, scene);
    leftLowerLeg.position = new BABYLON.Vector3(-0.12, -0.5, 0);
    leftLowerLeg.material = suitMaterial;
    
    const rightLowerLeg = BABYLON.MeshBuilder.CreateCylinder('rightLowerLeg', {height: 0.5, diameter: 0.1}, scene);
    rightLowerLeg.position = new BABYLON.Vector3(0.12, -0.5, 0);
    rightLowerLeg.material = suitMaterial;
    
    // Shoes
    const leftShoe = BABYLON.MeshBuilder.CreateBox('leftShoe', {width: 0.1, height: 0.05, depth: 0.15}, scene);
    leftShoe.position = new BABYLON.Vector3(-0.12, -0.77, 0.02);
    const shoeMat = new BABYLON.StandardMaterial('shoeMat', scene);
    shoeMat.diffuseColor = new BABYLON.Color3(0.05, 0.05, 0.05);
    leftShoe.material = shoeMat;
    
    const rightShoe = BABYLON.MeshBuilder.CreateBox('rightShoe', {width: 0.1, height: 0.05, depth: 0.15}, scene);
    rightShoe.position = new BABYLON.Vector3(0.12, -0.77, 0.02);
    rightShoe.material = shoeMat;
    
    // Add a tie
    const tie = BABYLON.MeshBuilder.CreateBox('tie', {width: 0.05, height: 0.4, depth: 0.01}, scene);
    tie.position = new BABYLON.Vector3(0, 0.95, 0.13);
    const tieMat = new BABYLON.StandardMaterial('tieMat', scene);
    tieMat.diffuseColor = new BABYLON.Color3(0, 0.5, 0);
    tieMat.emissiveColor = new BABYLON.Color3(0, 0.2, 0);
    tie.material = tieMat;
    
    // Create holographic particle system around avatar
    const particleSystem = new BABYLON.ParticleSystem('particles', 1000, scene);
    particleSystem.particleTexture = new BABYLON.Texture('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==', scene);
    
    // Create an invisible emitter that orbits around the avatar
    const emitter = BABYLON.MeshBuilder.CreateBox('emitter', {size: 0.01}, scene);
    emitter.visibility = 0;
    emitter.position.y = 1;
    particleSystem.emitter = emitter;
    
    particleSystem.minEmitBox = new BABYLON.Vector3(-0.5, -1, -0.5);
    particleSystem.maxEmitBox = new BABYLON.Vector3(0.5, 1, 0.5);
    
    particleSystem.color1 = new BABYLON.Color4(0, 1, 0, 0.8);
    particleSystem.color2 = new BABYLON.Color4(0, 0.8, 0.2, 0.5);
    particleSystem.colorDead = new BABYLON.Color4(0, 0, 0, 0);
    
    particleSystem.minSize = 0.01;
    particleSystem.maxSize = 0.03;
    
    particleSystem.minLifeTime = 1;
    particleSystem.maxLifeTime = 2;
    
    particleSystem.emitRate = 50;
    
    particleSystem.blendMode = BABYLON.ParticleSystem.BLENDMODE_ADD;
    
    particleSystem.gravity = new BABYLON.Vector3(0, 0.1, 0);
    
    particleSystem.direction1 = new BABYLON.Vector3(-0.5, 1, -0.5);
    particleSystem.direction2 = new BABYLON.Vector3(0.5, 1, 0.5);
    
    particleSystem.minEmitPower = 0.1;
    particleSystem.maxEmitPower = 0.3;
    particleSystem.updateSpeed = 0.01;
    
    particleSystem.start();
    
    // Animation - subtle human movements
    let time = 0;
    scene.registerBeforeRender(function () {
      time += 0.01;
      
      // Subtle head movement (looking around)
      head.rotation.y = Math.sin(time * 0.5) * 0.1;
      head.rotation.x = Math.sin(time * 0.3) * 0.05;
      
      // Blinking effect
      const blink = Math.sin(time * 3) > 0.98;
      if (blink) {
        leftEyeWhite.scaling.y = 0.1;
        rightEyeWhite.scaling.y = 0.1;
        leftIris.scaling.y = 0.1;
        rightIris.scaling.y = 0.1;
      } else {
        leftEyeWhite.scaling.y = 1;
        rightEyeWhite.scaling.y = 1;
        leftIris.scaling.y = 1;
        rightIris.scaling.y = 1;
      }
      
      // Eye movement (following invisible target)
      const eyeMovement = 0.01;
      leftIris.position.x = -0.1 + Math.sin(time * 0.7) * eyeMovement;
      rightIris.position.x = 0.1 + Math.sin(time * 0.7) * eyeMovement;
      leftPupil.position.x = -0.1 + Math.sin(time * 0.7) * eyeMovement;
      rightPupil.position.x = 0.1 + Math.sin(time * 0.7) * eyeMovement;
      
      // Breathing effect (chest movement)
      const breathe = Math.sin(time * 0.8) * 0.02;
      torso.scaling.z = 1 + breathe;
      torso.position.y = 0.8 + breathe * 0.5;
      
      // Subtle hand gesture
      rightLowerArm.rotation.z = -0.2 + Math.sin(time * 0.6) * 0.1;
      rightHand.position.y = 0.28 + Math.sin(time * 0.6) * 0.02;
      
      // Particle emitter orbit
      emitter.position.x = Math.sin(time * 0.5) * 1.5;
      emitter.position.z = Math.cos(time * 0.5) * 1.5;
      
      // Tie glow pulse
      const pulse = Math.sin(time * 2) * 0.5 + 0.5;
      tie.material.emissiveColor = new BABYLON.Color3(0, 0.2 * pulse, 0);
    });
    
    // Handle window resize
    window.addEventListener('resize', function () {
      engine.resize();
    });
    
    // Run render loop
    engine.runRenderLoop(function () {
      scene.render();
    });
    
    // Clean up on page unload
    window.addEventListener('beforeunload', function() {
      engine.dispose();
    });
  }
})();

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
</script>

---

<footer style="text-align: center; padding: 40px 20px; border-top: 1px solid rgba(0, 255, 0, 0.2); margin-top: 60px;">
  <p style="color: #888; font-size: 0.9em;">© 2025 AIMatrix. All rights reserved. | <a href="/privacy" style="color: #00ff00;">Privacy Policy</a> | <a href="/terms" style="color: #00ff00;">Terms of Service</a></p>
</footer>