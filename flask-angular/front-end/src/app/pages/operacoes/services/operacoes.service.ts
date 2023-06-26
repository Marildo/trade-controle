import { Injectable } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';



import { BaseAPIService } from 'src/app/service/api/base-api.service';


@Injectable({
  providedIn: 'root'
})
export class OperacoesService extends BaseAPIService {



  public load_dashboard(): Observable<any> {
    return this.get('operacoes/')
  }

  
  public load_statistics_daytrade(filter: Map<string, string>): Observable<any> {
    return this.get('operacoes/daytrade/statistics/',filter)
  }

  public load_detail(filter: Map<string, string>): Observable<any> {
    return this.get('operacoes/detail/', filter)
  }

  public load_summary(filter: Map<string, string>): Observable<any> {
    return this.get('operacoes/summary/', filter)
  }


  public load_files(filter: Map<string, string>): Observable<any> {
    return this.get('/notas/arquivos', filter)
  }

  search_files(): Observable<any> {
    const url = '/notas/arquivos/search' 
    return this.put(url)
  }

  public upload_file(files: File[]): Observable<any> {
    const formData: FormData = new FormData();
    const headers = new HttpHeaders({})
    let i = 0
    for (const file of files) {
      i++
      formData.append('file'+i, file);  
    }
    return this.post('/notas/arquivos', formData, headers)    
  }

  public process_file(file_id: string): Observable<any> {
    const url = '/notas/arquivos/' + file_id
    return this.put(url)
  }
}
