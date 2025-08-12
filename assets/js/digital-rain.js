// Digital Rain Effect for AIMatrix Documentation
// Following the exact algorithm from tmp/index.html

(function() {
  // Wait for DOM to be ready
  function initDigitalRain() {
    // Create canvas element
    const canvas = document.createElement('canvas');
    canvas.id = 'digital-rain-canvas';
    canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;';
    
    // Insert canvas as first element in body
    document.body.insertBefore(canvas, document.body.firstChild);
    
    const context = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Character sets - using only Greek letters and 'aimatrix.com' as per original
    const greekletter = 'αβγδεζηθικλμνξοπρστυφχψω';
    const lowercaseletter = 'aimatrix.com';
    const alphabet = greekletter + lowercaseletter;
    
    const fontSize = 16;
    const columns = canvas.width/fontSize;
    
    const rainDrops = [];
    
    // Initialize rain drops with random positions to avoid vertical line at start
    for(let x = 0; x < columns; x++) {
      rainDrops[x] = Math.floor(Math.random() * -100);
    }
    
    // Draw function - exact algorithm from original
    const draw = () => {
      // Fade effect with black overlay
      context.fillStyle = 'rgba(0, 0, 0, 0.05)';
      context.fillRect(0, 0, canvas.width, canvas.height);
      
      // Green color with 0.48 opacity (20% brighter than 0.4)
      context.fillStyle = 'rgba(0, 255, 0, 0.48)';
      context.font = fontSize + 'px monospace';
      
      for(let i = 0; i < rainDrops.length; i++) {
        const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
        context.fillText(text, i*fontSize, rainDrops[i]*fontSize);
        
        if(rainDrops[i]*fontSize > canvas.height && Math.random() > 0.975) {
          rainDrops[i] = 0;
        }
        rainDrops[i]++;
      }
    };
    
    // Run animation - using 200ms interval (2x slower)
    setInterval(draw, 200);
    
    // Handle window resize
    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });
    
    console.log('Digital rain effect initialized with Greek letters - bright green');
  }
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDigitalRain);
  } else {
    initDigitalRain();
  }
})();