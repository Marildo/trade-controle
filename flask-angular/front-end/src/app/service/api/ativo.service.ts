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

}
