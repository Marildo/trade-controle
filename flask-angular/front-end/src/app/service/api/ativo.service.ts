import { Injectable } from '@angular/core';

import { BaseAPIService } from 'src/app/service/api/base-api.service';
import { Observable, map, take, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AtivoService extends BaseAPIService {

  protected path = "ativos";

  public loadAll(): Observable<any> {
    return this.get(this.path)
  }


  public runBacktest(body: any): Observable<any> {
    return this.post(this.path + '/backtest', body)
  }

  runBacktestToCsv(body: any): Observable<any> {
    this.loader.show()
    const full_url = this.baseURL + this.path + '/backtest/csv'
    return this.http.post(full_url, body,
      {
        headers: this.headers != null ? this.headers : this.headers,
        responseType: 'blob'
      }
    ).pipe(
      take(1),
      tap((resp: any) => {
        this.loader.hide()
      }),      
    );
    
  }
}
