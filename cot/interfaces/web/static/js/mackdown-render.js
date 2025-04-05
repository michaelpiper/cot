class MarkdownRenderer {
  /**
   * 
   * @param {HTMLElement} containerId 
   */
  constructor(container) {
    this.container = container;
  }

  render(markdownContent) {
    const html = MarkdownParser.toHTML(markdownContent);
    this.container.innerHTML = html;
  }

  append(markdownContent) {
    const html = MarkdownParser.toHTML(markdownContent);
    const temp = document.createElement('div');
    temp.innerHTML = html;

    while (temp.firstChild) {
      this.container.appendChild(temp.firstChild);
    }
  }
}
