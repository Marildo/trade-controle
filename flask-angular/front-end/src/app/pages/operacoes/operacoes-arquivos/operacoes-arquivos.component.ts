import { query } from '@angular/animations';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { OperacoesService } from 'src/app/pages/operacoes/services/operacoes.service';



@Component({
  selector: 'app-operacoes-arquivos',
  templateUrl: './operacoes-arquivos.component.html',
  styleUrls: ['./operacoes-arquivos.component.scss']
})
export class OperacoesArquivosComponent {

  public hiddenForm = true;
  public items: any[];
  public selectedFile!: File | null;

  public tipoNota!:string;
  public start_processamento!:any;
  public end_processamento!:any;

  private filter = new Map();



  constructor(private router: Router, private service: OperacoesService) {
    const today = new Date()
    const day = today.getDay();
    const diff = today.getDate() - day + (day === 0 ? -6 : 0); 
    this.start_processamento = new Date(today.setDate(diff)).toISOString().split('T')[0];
    this.end_processamento=   new Date().toISOString().split('T')[0];


    this.items = [];
    this.tipoNota='-1';
  }

  ngOnInit(): void {
    this.onLoad()
  }



  private onLoad(): void {
    if(this.start_processamento != ''){
      this.filter.set('start_processamento',this.start_processamento)
    }
    if (this.end_processamento != ''){
      this.filter.set('end_processamento',this.end_processamento)
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
    this.selectedFile = event.target.files[0];
  }

  onSelectTypeNota(tipo: any):void {
    if (tipo == '-1'){
      this.filter.clear()
    }else{
      this.filter.set('tipo',tipo)
    }

    this.onLoad()
  }

  onFilterDates(){  
    this.onLoad()
  }

  onUploadFile() {
    if (this.selectedFile) {
      this.service.upload_file(this.selectedFile)
        .subscribe({
          next: (resp) => {
            console.log(resp)
            this.onView(resp.data.id)
          },
          error: (e) => {
            console.log(e.error)
          }
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
          console.error(e)
        }
      })
  }
}



 