import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { take, map, tap } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class OperacoesService {

  constructor(private http: HttpClient) { }

  public load(): Observable<any>{
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    })

    let url ='http://127.0.0.1:7500/operacoes/?encerrada=1&data_encerramento=2020-12-30'
    return this.http.get<any>(url, {headers})
      .pipe(
        take(1), // apenas um chamada
        // delay(5000),
       //map(i => i.data),
       //tap(console.log),
      )
  }
}
