import { Component, OnInit, Input } from '@angular/core';

import { ReportInputFileDto } from './utils/models/report-InputFile.dto';
import { ReportInputFileService } from './utils/services/report-input-file.service';
import { RoutingService } from '@app/core/services/Routing/routing.services';
import { UserService } from '../../../../login/user-authenticate-service';
import { FileService } from '../../../../shell/shell-routing-service';
import { SessionToHistoryService } from '../../session-to-history.service';
import { Router } from '@angular/router';
import { fromPairs } from 'lodash';
import { listLazyRoutes } from '@angular/compiler/src/aot/lazy_routes';
import { NzTableFilterFn, NzTableFilterList, NzTableSortFn, NzTableSortOrder } from 'ng-zorro-antd/table';
interface DataItem {
  name: string;
  age: number;
  address: string;
}
interface ColumnItem {
  name: string;

  listOfFilter: NzTableFilterList;
  filterFn: NzTableFilterFn | null;
}
@Component({
  selector: 'app-report-input-file',
  templateUrl: './report-input-file.component.html',
  styleUrls: ['./report-input-file.component.scss'],
})
export class ReportInputFileComponent implements OnInit {
  @Input() SessionList: any;
  columnFilter: ColumnItem = {
    name: 'Trạng thái',
    listOfFilter: [
      { text: 'Success', value: 'Success' },
      { text: 'Loading', value: 'Loading' },
      { text: 'Fail', value: 'Fail' },
    ],

    filterFn: (statusList: string[], item: any) => statusList.indexOf(item.Status) !== -1,
  };
  columnFilter2: ColumnItem = {
    name: 'Loại so sánh',
    listOfFilter: [
      { text: 'Multiple files', value: 'Multiple files' },
      { text: 'Database', value: 'Database' },
      { text: 'Internet', value: 'Internet' },
      { text: 'Database and Internet', value: ' Database and Internet' },
    ],
    filterFn: (typeList: string[], item: any) => typeList.indexOf(item.SessionType) !== -1,
  };

  filterFn: NzTableFilterFn | null;
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
      //this.loading = false;
      setTimeout(() => {
        this.displayData = data.session;
        this.ListOfTemp = data.session;

        let sort = {
          key: 'Date',
          value: 'descend',
        };
        this.sort(sort);
        this.Warning(this.ListOfTemp[0]);
      }, 3000);
    });
  }
  Warning(sample: any) {
    this.loading = false;
    let data = {
      sessionId: sample.id,
      filename: sample.filename,
    };

    localStorage.setItem('sesstionId', sample.id);
    this.sessionToHistoryService.sendFileList(data);
  }
  // Routing
  goToDetail(event: any): void {
    this.routingService.navigateToUpdate('/daovan/', event.id);
  }
  /*
  getReportInputFile(): void {
    this.reportInputFileService.getJSON().subscribe((res: any) => {
      setTimeout(() => {
        this.loading = false;
        this.reportInputFile = res;
        for (var i = 0; i < this.reportInputFile.length; i++) {
          console.log(this.reportInputFile[i]);
        }
      }, 3000);
    });
  }
*/
  //#region
  sort(sort: { key: string; value: string }): void {
    this.sortName = sort.key;
    this.sortValue = sort.value;
    this.search();
  }

  search(): void {
    // sort data
    if (this.sortName && this.sortValue) {
      this.displayData = this.displayData.sort((a, b) =>
        this.sortValue === 'ascend'
          ? a[this.sortName] > b[this.sortName]
            ? 1
            : -1
          : b[this.sortName] > a[this.sortName]
          ? 1
          : -1
      );
    } else {
      this.displayData = this.displayData;
    }
  }
  //#endregion
}
