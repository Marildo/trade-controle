import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { BaseAPIService } from 'src/app/service/api/base-api.service';


@Injectable({
  providedIn: 'root'
})
export class CarteiraService extends BaseAPIService {

  protected path = "carteiras/";

  public loadAll(): Observable<any> {
    return this.get(this.path)
  }

  public update(body: any): Observable<any> {
    return this.put(this.path, body)
  }


  public save(body: any): Observable<any> {
    return this.post(this.path, body)
  }

  public saveMovimentacao(body: any): Observable<any> {
    return this.post(this.path + 'movimentacoes', body)
  }

  public load_movimentacoes(): Observable<any> {
    return this.get(this.path + 'movimentacoes')
  }

}