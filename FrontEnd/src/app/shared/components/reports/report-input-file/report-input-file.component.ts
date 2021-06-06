import { Component, OnInit, Input } from '@angular/core';

import { ReportInputFileDto } from './utils/models/report-InputFile.dto';
import { ReportInputFileService } from './utils/services/report-input-file.service';
import { RoutingService } from '@app/core/services/Routing/routing.services';
import { UserService } from '../../../../login/user-authenticate-service';
import { FileService } from '../../../../shell/shell-routing-service';
import { SessionToHistoryService } from '../../session-to-history.service';
import { Router } from '@angular/router';
import { fromPairs } from 'lodash';

@Component({
  selector: 'app-report-input-file',
  templateUrl: './report-input-file.component.html',
  styleUrls: ['./report-input-file.component.scss'],
})
export class ReportInputFileComponent implements OnInit {
  @Input() SessionList: any;
  loading = true;
  reportInputFile: ReportInputFileDto[] = [];
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  ListOfTemp: any[];
  constructor(
    private reportInputFileService: ReportInputFileService,
    private routingService: RoutingService,
    private userService: UserService,
    private fileService: FileService,
    private router: Router,
    private sessionToHistoryService: SessionToHistoryService
  ) {}
  ngOnChanges() {
    this.loading = false;
  }
  ngOnInit(): void {
    this.userService.getSession(localStorage.getItem('id')).subscribe((data: any) => {
      console.log(data);
      //this.loading = false;
      setTimeout(() => {
        this.displayData = data.session;
        this.ListOfTemp = data.session;
        console.log('this is');
        this.Warning(0);
      }, 3000);
    });

    //this.getReportInputFile();
  }
  Warning(id: number) {
    this.loading = false;
    let data = {
      //'id':localStorage.getItem('id'),
      sessionId: id,
      filename: this.ListOfTemp[id].filename,
    };
    localStorage.setItem('sesstionId', id.toString());
    this.sessionToHistoryService.sendFileList(data);
    // this.fileService.getResult(data).subscribe((data:any)=>{
    //   //this.router.navigate('daovan',{})
    // })
  }
  // Routing
  goToDetail(event: any): void {
    console.log(event);
    this.routingService.navigateToUpdate('/daovan/', event.id);
  }

  getReportInputFile(): void {
    this.reportInputFileService.getJSON().subscribe((res: any) => {
      setTimeout(() => {
        this.loading = false;
        console.log(res);
        this.reportInputFile = res;
        for (var i = 0; i < this.reportInputFile.length; i++) {
          console.log(this.reportInputFile[i]);
        }
      }, 3000);
    });
  }

  //#region
  sort(sort: { key: string; value: string }): void {
    this.sortName = sort.key;
    this.sortValue = sort.value;
    this.search();
  }

  search(): void {
    // sort data
    if (this.sortName && this.sortValue) {
      this.displayData = this.reportInputFile.sort((a, b) =>
        this.sortValue === 'ascend'
          ? a[this.sortName] > b[this.sortName]
            ? 1
            : -1
          : b[this.sortName] > a[this.sortName]
          ? 1
          : -1
      );
    } else {
      this.displayData = this.reportInputFile;
    }
  }
  //#endregion
}
