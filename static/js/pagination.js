class Pagination {
    constructor(options) {
        this.currentPage = options.currentPage || 1;
        this.totalPages = options.totalPages || 1;
        this.onPageChange = options.onPageChange || (() => {});
        this.visiblePages = options.visiblePages || 10;
        this.container = options.container;
        
        this.init();
    }
    
    init() {
        this.render();
        this.attachEventListeners();
    }
    
    calculateVisibleRange() {
        const halfVisible = Math.floor(this.visiblePages / 2);
        let start = Math.max(1, this.currentPage - halfVisible);
        let end = Math.min(this.totalPages, start + this.visiblePages - 1);
        
        // Ajustar el inicio si estamos cerca del final
        if (end === this.totalPages) {
            start = Math.max(1, end - this.visiblePages + 1);
        }
        
        return { start, end };
    }
    
    render() {
        const { start, end } = this.calculateVisibleRange();
        let html = `
            <nav aria-label="Navegación de páginas">
                <ul class="pagination justify-content-center">
                    <li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                        <a class="page-link" href="#" data-page="${this.currentPage - 1}" aria-label="Anterior">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
        `;
        
        // Primera página
        if (start > 1) {
            html += `
                <li class="page-item">
                    <a class="page-link" href="#" data-page="1">1</a>
                </li>
            `;
            if (start > 2) {
                html += `
                    <li class="page-item disabled">
                        <span class="page-link">...</span>
                    </li>
                `;
            }
        }
        
        // Páginas visibles
        for (let i = start; i <= end; i++) {
            html += `
                <li class="page-item ${i === this.currentPage ? 'active' : ''}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                </li>
            `;
        }
        
        // Última página
        if (end < this.totalPages) {
            if (end < this.totalPages - 1) {
                html += `
                    <li class="page-item disabled">
                        <span class="page-link">...</span>
                    </li>
                `;
            }
            html += `
                <li class="page-item">
                    <a class="page-link" href="#" data-page="${this.totalPages}">${this.totalPages}</a>
                </li>
            `;
        }
        
        html += `
                    <li class="page-item ${this.currentPage === this.totalPages ? 'disabled' : ''}">
                        <a class="page-link" href="#" data-page="${this.currentPage + 1}" aria-label="Siguiente">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                </ul>
            </nav>
        `;
        
        this.container.innerHTML = html;
    }
    
    attachEventListeners() {
        this.container.addEventListener('click', (e) => {
            e.preventDefault();
            
            const target = e.target.closest('.page-link');
            if (!target) return;
            
            const page = parseInt(target.dataset.page);
            if (page && page !== this.currentPage && page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
                this.render();
                this.onPageChange(page);
            }
        });
    }
    
    update(options) {
        if (options.currentPage) this.currentPage = options.currentPage;
        if (options.totalPages) this.totalPages = options.totalPages;
        if (options.onPageChange) this.onPageChange = options.onPageChange;
        this.render();
    }
} 