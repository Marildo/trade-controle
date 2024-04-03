import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { BaseAPIService } from './base-api.service';
import { take, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SetupService extends BaseAPIService {

  protected path = "setups";

  public loadAll(): Observable<any> {
    return this.get(this.path)
  }

  public save(body: any): Observable<any> {
    return this.post(this.path, body)
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

  public indiceFut(): Observable<any> {
    return this.get(this.path + '/indfut')
  }
}