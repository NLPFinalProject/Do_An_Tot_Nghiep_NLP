import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

// const routes = {
//   ReportInputFire: () => `${MookData}`
// };
@Injectable({
  providedIn: 'root',
})
export class ListAccountService {
  mookData = 'http://localhost:4200/assets/mookdata/mookUsers.json';
  constructor(private http: HttpClient) {}

  public getJSON(): Observable<any> {
    return this.http.get(this.mookData).pipe(
      map((body: any) => body.json()),
      catchError(() => of('Error, could not load file jsonaaaaaaaaaaaaaaaaaaaaaaaaa :-('))
    );
  }
}
