import { Component, OnInit, Input } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';
import { DaovanServiceService } from '../../daovan-service.service';
@Component({
  selector: 'app-list-file-diff',
  templateUrl: './list-file-diff.component.html',
  styleUrls: ['./list-file-diff.component.scss'],
})
export class ListFileDiffComponent implements OnInit {
  @Input() FileList2: Array<any>;
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  loading = true;
  data = [{}];
  fileList: Array<object> = [];
  constructor(private messageService: MessageService, private DaoVanService: DaovanServiceService) {}
  ngOnInit(): void {
    this.getData();
  }
  ngOnChanges() {
    //this.childFunction()

    this.getData();
  }
  getData(): void {
    const number = Math.floor(Math.random() * 100);
    setTimeout(() => {
      this.displayData = [...this.FileList2];
      this.loading = false;
    }, number);
  }
  sendMessage(name: string) {
    for (var i = 0; i < this.FileList2.length; i++) {
      if (this.FileList2[i].name == name) {
        this.DaoVanService.getSetting(i);
        break;
      }
    }
  }
  sort(sort: { key: string; value: string }): void {
    this.sortName = sort.key;
    this.sortValue = sort.value;
    this.search();
  }

  search(): void {
    // filter data
    const filterFunc = (item: any) =>
      (this.searchAddress ? item.address.indexOf(this.searchAddress) !== -1 : true) &&
      (this.listOfSearchName.length
        ? this.listOfSearchName.some((name: string) => item.name.indexOf(name) !== -1)
        : true);
    const data = this.data.filter((item) => filterFunc(item));
    // sort data
    if (this.sortName && this.sortValue) {
      this.displayData = data.sort((a, b) =>
        this.sortValue === 'ascend'
          ? a[this.sortName] > b[this.sortName]
            ? 1
            : -1
          : b[this.sortName] > a[this.sortName]
          ? 1
          : -1
      );
    } else {
      this.displayData = data;
    }
  }
}
