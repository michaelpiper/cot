// markdown.js
class MarkdownParser {
    static toHTML(markdown) {
      // Basic Markdown conversions
      let html = markdown
        // Headers
        .replace(/^# (.*$)/gm, '<h1>$1</h1>')
        .replace(/^## (.*$)/gm, '<h2>$1</h2>')
        .replace(/^### (.*$)/gm, '<h3>$1</h3>')
        
        // Bold/Italic
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        
        // Links
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>')
        
        // Lists
        .replace(/^\s*\*\s(.*$)/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
        
        // Paragraphs (ensure wrapped in <p> tags)
        .replace(/^(?!<[a-z])(.*$)/gm, '<p>$1</p>')
        
        // Line breaks
        .replace(/\n/g, '<br>');
  
      return html;
    }
}