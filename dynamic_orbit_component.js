// TODO: make the base URL for content_ids configurable so that people can host from their own servers if desired.
class DynamicOrbit extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  async connectedCallback() {
    await this.loadOrbitComponents();
    const content_id = this.getAttribute("content_id");
    this.color = this.getAttribute("color") ?? "blue";
    this.flashcards = await this.fetchFlashcards(content_id);
    this.render();
  }

  async loadOrbitComponents() {
    if (!customElements.get("orbit-reviewarea")) {
      await import("https://js.withorbit.com/orbit-web-component.js");
    }
  }

  async fetchFlashcards(content_id) {
    // Fetch flashcards from your static content server
    const response = await fetch(`${content_id}`);
    return await response.json();
  }

  render() {
    this.shadowRoot.innerHTML = `
        <orbit-reviewarea color="${this.color}">
          ${this.flashcards.cards
            .map(
              (card) => `
            <orbit-prompt
              question="${card.front}"
              answer="${card.back}"
            ></orbit-prompt>
          `,
            )
            .join("")}
        </orbit-reviewarea>
      `;
  }
}

customElements.define("dynamic-orbit", DynamicOrbit);
