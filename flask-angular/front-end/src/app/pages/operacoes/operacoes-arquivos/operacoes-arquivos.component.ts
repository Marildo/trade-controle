import { query } from '@angular/animations';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { OperacoesService } from 'src/app/services/operacoes.service';



@Component({
  selector: 'app-operacoes-arquivos',
  templateUrl: './operacoes-arquivos.component.html',
  styleUrls: ['./operacoes-arquivos.component.scss']
})
export class OperacoesArquivosComponent {

  public hiddenForm = true;
  public items: any[];
  public selectedFile!: File | null;

  private filter = new Map();
 


  constructor(private router: Router, private service: OperacoesService) {
    this.items = [];
  }

  ngOnInit(): void {
    this.hiddenForm = false;
    this.onLoad()
  }



  private onLoad(): void {
    this.hiddenForm = false;

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

  onUploadFile() {
     if(this.selectedFile){
      this.service.upload_file(this.selectedFile)
      .subscribe({
        next: (resp) => {
          this.onLoad()
        },
        error: (e) => {
          console.error(e)
        }
      })
     }
  }

  onProcessFile(id: string): void {
    this.service.process_file(id)
      .subscribe({
        next: (resp) => {
          this.onLoad()
        },
        error: (e) => {
          console.error(e)
        }
      })
  }
}
