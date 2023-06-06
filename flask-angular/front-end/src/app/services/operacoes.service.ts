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

  public load_opened(start: String): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    })

    const periodo = start != '' ? '&data_encerramento=' + start : '';

    let url = 'http://127.0.0.1:7500/operacoes/opened/?' + periodo
    return this.http.get<any>(url, { headers })
      .pipe(
        take(1), // apenas um chamada
        // delay(5000),
        //map(i => i.data),
        tap(console.log),
      )
  }
}
