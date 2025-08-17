// CloudFront Function to handle clean URLs for S3 static site
// This function appends index.html to directory requests

function handler(event) {
    var request = event.request;
    var uri = request.uri;
    
    // Check if the URI ends with a slash (directory request)
    if (uri.endsWith('/')) {
        request.uri += 'index.html';
    } 
    // Check if the URI doesn't have a file extension (likely a directory)
    else if (!uri.includes('.')) {
        // Check if we should append /index.html
        // Don't modify if it's likely an API endpoint or special path
        if (!uri.startsWith('/api/') && !uri.startsWith('/_')) {
            request.uri += '/index.html';
        }
    }
    
    return request;
}