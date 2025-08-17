// CloudFront Function to handle clean URLs for S3 static site
// This function appends index.html to directory requests

function handler(event) {
    var request = event.request;
    var uri = request.uri;
    
    // If URI is just '/', append index.html
    if (uri === '/') {
        request.uri = '/index.html';
    }
    // If URI ends with '/', append index.html
    else if (uri.endsWith('/')) {
        request.uri = uri + 'index.html';
    }
    // If URI doesn't have a file extension, append /index.html
    else if (uri.lastIndexOf('.') < uri.lastIndexOf('/') || uri.lastIndexOf('.') === -1) {
        // Don't modify API or special paths
        if (!uri.startsWith('/api/') && !uri.startsWith('/_')) {
            request.uri = uri + '/index.html';
        }
    }
    
    return request;
}