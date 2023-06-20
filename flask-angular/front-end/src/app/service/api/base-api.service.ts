import { HttpClient, HttpHeaders, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { take, map, tap, catchError } from 'rxjs/operators';

import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BaseAPIService {

  protected baseURL: string;
  protected headers: HttpHeaders;

  constructor(protected http: HttpClient) {
    this.baseURL = environment.apiUrl
    this.headers = new HttpHeaders({
      'Content-Type': 'application/json',
    })
  }

  public get(url: string, filter: Map<string, string> = new Map(), headers: HttpHeaders | null = null): Observable<any> {
    const full_url = this.baseURL + url
    let params = new HttpParams();
    filter.forEach((k, v) => {
      params = params.set(v, k);
    });

    const options = { headers: headers != null ? headers : this.headers, params }
    return this.http.get<any>(full_url, options)
      .pipe(
        take(1),
        tap(console.log),
        catchError(this.handleError)
      )
  }

  public post(url: string, body: any, headers: HttpHeaders | null = null): Observable<any> {
    const full_url = this.baseURL + url
    const options = { headers: headers != null ? headers : this.headers }
    return this.http.post<any>(full_url, body, options)
      .pipe(
        take(1),
        tap(console.log),
        catchError(this.handleError)
      )
  }

  public put(url: string, body: any | null = null, headers: HttpHeaders | null = null): Observable<any> {
    const full_url = this.baseURL + url
    const options = { headers: headers != null ? headers : this.headers }
    return this.http.put<any>(full_url, body, options)
      .pipe(
        take(1),
        tap(console.log),
        catchError(this.handleError)
      )
  }


  handleError(exception: HttpErrorResponse) {
    console.error(exception)
    return throwError('An error occurred');
  }
}
