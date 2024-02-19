import { HttpClient, HttpHeaders, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { take, map, tap, catchError } from 'rxjs/operators';
import { LoaderService } from 'src/app/components/loader/loader.service';

import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BaseAPIService {

  protected baseURL: string;
  protected headers: HttpHeaders;

  constructor(protected http: HttpClient, protected loader: LoaderService) {
    this.baseURL = environment.apiUrl
    this.headers = new HttpHeaders({
      'Content-Type': 'application/json',
    })
  }

  public get(url: string, filter: Map<string, string> = new Map(), headers: HttpHeaders | null = null): Observable<any> {
    this.loader.show()
    const full_url = this.baseURL + url
    let params = new HttpParams();
    const isNullOrEmpty = (str: string | null | undefined): boolean => str === null || str === undefined || str === '';
    filter.forEach((v, k) => {
      if (!isNullOrEmpty(v)) {
        console.log(k, v)
        params = params.set(k, v);
      }
    });

    const options = { headers: headers != null ? headers : this.headers, params }
    return this.http.get<any>(full_url, options)
      .pipe(
        take(1),
        tap({
          next: (data) => console.log(data),
          error: (error) => {
            console.error(error)
            this.loader.hide()
          },
          complete: () => this.loader.hide()
        })
      )
  }

  public post(url: string, body: any, headers: HttpHeaders | null = null): Observable<any> {
    this.loader.show()
    const full_url = this.baseURL + url
    const options = { headers: headers != null ? headers : this.headers }
    return this.http.post<any>(full_url, body, options)
      .pipe(
        take(1),
        tap({
          next: (data) => console.log(data),
          error: (error) => {
            console.error(error)
            this.loader.hide()
          },
          complete: () => this.loader.hide()
        })
      )
  }

  public put(url: string, body: any | null = null, headers: HttpHeaders | null = null): Observable<any> {
    this.loader.show()
    const full_url = this.baseURL + url
    const options = { headers: headers != null ? headers : this.headers }
    return this.http.put<any>(full_url, body, options)
      .pipe(
        take(1),
        tap({
          next: (data) => console.log(data),
          error: (error) => {
            console.error(error)
            this.loader.hide()
          },
          complete: () => this.loader.hide()
        })
      )
  }

  public patch(url: string, body: any | null = null, headers: HttpHeaders | null = null): Observable<any> {
    this.loader.show()
    const full_url = this.baseURL + url
    const options = { headers: headers != null ? headers : this.headers }
    return this.http.patch<any>(full_url, body, options)
      .pipe(
        take(1),
        tap({
          next: (data) => console.log(data),
          error: (error) => {
            console.error(error)
            this.loader.hide()
          },
          complete: () => this.loader.hide()
        })
      )
  }

}


