import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../../../../../../environments/environment';
// const routes = {
//   ReportInputFire: () => `${MookData}`
// };
@Injectable({
  providedIn: 'root',
})
export class ReportInputFileService {
  tempoLocalData = 'http://localhost:4200';
  mookData = this.tempoLocalData + '/assets/mookdata/reportInputFile.json';
  constructor(private http: HttpClient) {}

  public getJSON(): Observable<any> {
    return this.http.get(this.mookData).pipe(
      map((body: any) => body),
      catchError(() => of('Error, could not load file json :-('))
    );
  }
}
