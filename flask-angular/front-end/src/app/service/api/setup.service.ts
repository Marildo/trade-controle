import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { BaseAPIService } from './base-api.service';

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
}