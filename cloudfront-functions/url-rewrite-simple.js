function handler(event) {
    var request = event.request;
    var uri = request.uri;
    
    // If URI ends with '/', append 'index.html'
    if (uri.endsWith('/')) {
        request.uri = uri + 'index.html';
    }
    
    return request;
}