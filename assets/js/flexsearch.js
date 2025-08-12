// FlexSearch configuration for Hextra theme
document.addEventListener('DOMContentLoaded', function() {
  // Initialize FlexSearch with custom configuration
  const searchConfig = {
    encode: "icase",
    tokenize: "forward",
    threshold: 0,
    resolution: 3,
    depth: 3,
    cache: 100,
    worker: false,
    doc: {
      id: "id",
      field: ["title", "content", "description"],
      store: ["title", "content", "url", "description"]
    }
  };

  // Create search index
  window.searchIndex = new FlexSearch.Document(searchConfig);
  
  // Load search data
  fetch('/index.json')
    .then(response => response.json())
    .then(data => {
      data.forEach((item, index) => {
        window.searchIndex.add({
          id: index,
          title: item.title || '',
          content: item.content || '',
          description: item.description || '',
          url: item.permalink || item.url || ''
        });
      });
    })
    .catch(error => console.error('Error loading search index:', error));
});