import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { take, map, tap, catchError } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class OperacoesService {


  private baseURL = 'http://127.0.0.1:7500';

  private headers: HttpHeaders;


  constructor(private http: HttpClient) {
    this.headers = new HttpHeaders({
      'Content-Type': 'application/json',
    })

  }

  public load_detail(filter: Map<string, string>): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    })

    let params = new HttpParams();
    filter.forEach((k, v) => {
      params = params.set(v, k);
    });

    const options = { headers, params }

    let url = 'http://127.0.0.1:7500/operacoes/detail/'
    return this.http.get<any>(url, options)
      .pipe(
        take(1), // apenas um chamada
        // delay(5000),
        //map(i => i.data),
        tap(console.log),
      )
  }

  public load_summary(filter: Map<string, string>): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    })

    let params = new HttpParams();
    filter.forEach((k, v) => {
      params = params.set(v, k);
    });

    const options = { headers, params }
    const url = 'http://127.0.0.1:7500/operacoes/summary/'
    return this.http.get<any>(url, options)
      .pipe(

        take(1),
        tap(console.log),

      )
  }


  public load_files(filter: Map<string, string>): Observable<any> {
    let params = new HttpParams();
    filter.forEach((k, v) => {
      params = params.set(v, k);
    });

    const options = { headers: this.headers, params }
    const url = this.baseURL + '/notas/arquivos'
    return this.http.get<any>(url, options)
      .pipe(
        take(1),
        tap(console.log),
      )
  }

  upload_file(file: File) : Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'multipart/form-data'
    })

    const options = { headers: headers}

    const formData:FormData = new FormData();
 
    formData.append('file', file);
    formData.forEach((value, key) => {
      console.log(key, value);
    });

    const url = this.baseURL + '/notas/arquivos'

    return this.http.post<any>(url, formData)
    .pipe(
      take(1),
      tap(console.log),
    )
  }

  public process_file(file_id: string): Observable<any> {

    const options = { headers: this.headers}
    const url = this.baseURL + '/notas/arquivos/'+file_id
    return this.http.put<any>(url, options)
      .pipe(
        take(1),
        tap(console.log),
      )
  }
}
