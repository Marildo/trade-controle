import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ModalService } from 'src/app/components/modal/modal-service';

import { OperacoesService } from 'src/app/pages/operacoes/services/operacoes.service';


@Component({
  selector: 'app-operacoes-arquivos',
  templateUrl: './operacoes-arquivos.component.html',
  styleUrls: ['./operacoes-arquivos.component.scss']
})
export class OperacoesArquivosComponent {
  private modalArquivos = 'modalArquivos'

  public hiddenForm = true;
  public items: any[];
  public uploadedFiles: any[];



  public selectedFiles!: File[] | null;

  public tipoNota!: string;
  public start_processamento!: any;
  public end_processamento!: any;
  public start_referencia!: any;
  public end_referencia!: any;

  private filter = new Map();



  constructor(private router: Router,
    private service: OperacoesService,
    private messageService: MessageService,
    private modalService: ModalService) {
    const today = new Date()
    const day = today.getDay();
    const diff = today.getDate() - day + (day === 0 ? -6 : 0);
    this.start_referencia = new Date(today.setDate(diff)).toISOString().split('T')[0];
    // this.end_referencia = new Date().toISOString().split('T')[0];

    //this.start_processamento = new Date().toISOString().split('T')[0];
    //this.end_processamento = new Date().toISOString().split('T')[0];


    this.items = [];
    this.uploadedFiles = [];
    this.tipoNota = '-1';
  }

  ngOnInit(): void {
    this.onLoad()
  }


  private onLoad(): void {
    if (this.start_processamento != undefined) {
      this.filter.set('start_processamento', this.start_processamento)
    }
    if (this.end_processamento != undefined) {
      this.filter.set('end_processamento', this.end_processamento)
    }


    if (this.start_referencia != undefined) {
      this.filter.set('start_referencia', this.start_referencia)
    }

    if (this.end_referencia != undefined) {
      this.filter.set('end_referencia', this.end_referencia)
    }

    this.service.load_files(this.filter)
      .subscribe({
        next: (resp) => {
          this.items = resp.data
        },
        error: (e) => {
          console.error(e)
        }
      })
  }


  onView(id: string): void {
    const params = { file_id: id };
    this.router.navigate(['operacoes/detalhe'], { queryParams: params })
  }

  onSelectFile(event: any) {
    this.selectedFiles = event.target.files;
  }

  onSelectTypeNota(tipo: any): void {
    if (tipo == '-1') {
      this.filter.clear()
    } else {
      this.filter.set('tipo', tipo)
    }

    this.onLoad()
  }

  onFilterDates() {
    this.onLoad()
  }

  onSearchCorretora() {
    this.service.search_files()
      .subscribe({
        next: (resp) => {
          this.uploadedFiles = resp.data.notas
          this.modalService.open(this.modalArquivos)
        },
        error: e => this.messageService.add({ severity: 'error', summary: 'Erro', detail: e.error.message, life: 5000 })
      })
  }

  onUploadFile() {
    if (this.selectedFiles) {
      this.service.upload_file(this.selectedFiles)
        .subscribe({
          next: (resp) => {
            this.uploadedFiles = resp.data
            this.modalService.open(this.modalArquivos)
          },
          error: e => this.messageService.add({ severity: 'error', summary: 'Erro', detail: e.error.message, life: 5000 })
        })
    }
  }

  onProcessFile(id: string): void {
    this.service.process_file(id)
      .subscribe({
        next: (resp) => {
          this.onView(id)
        },
        error: (e) => {
          this.messageService.add({ severity: 'error', summary: 'Erro', detail: e.error.message, life: 5000 });
        }
      })
  }

  onCloseModalArquivos() {
    this.modalService.close(this.modalArquivos)
  }
}



