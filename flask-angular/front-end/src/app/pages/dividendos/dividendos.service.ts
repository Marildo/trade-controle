import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { BaseAPIService } from 'src/app/service/api/base-api.service';

@Injectable({
  providedIn: 'root'
})
export class DividendosService extends BaseAPIService{

  public load_all(): Observable<any> {
    return this.get('dividendos/')
  }

}
