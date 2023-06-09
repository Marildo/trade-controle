import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { take, map, tap } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class OperacoesService {

  constructor(private http: HttpClient) { }

  public load_closed(start: string, ativo: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    })


    const periodo = start != '' ? '&data_encerramento=' + start : '';
    const ativo_id = ativo != '' ? '&ativo_id=' + ativo : '';


    let url = 'http://127.0.0.1:7500/operacoes/closed/?' + periodo + ativo_id
    return this.http.get<any>(url, { headers })
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
    filter.forEach((k,v) => {
      params = params.set(v,k);
    });

    const options = { headers, params }
    const url = 'http://127.0.0.1:7500/operacoes/summary/'
    return this.http.get<any>(url, options)
      .pipe(
        take(1),
        tap(console.log),
      )
  }
}
