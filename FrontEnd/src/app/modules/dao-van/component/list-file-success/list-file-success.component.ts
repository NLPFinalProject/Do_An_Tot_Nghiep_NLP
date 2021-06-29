import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-list-file-success',
  templateUrl: './list-file-success.component.html',
  styleUrls: ['./list-file-success.component.scss'],
})
export class ListFileSuccessComponent implements OnInit {
  @Input() File1Name: any;
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  loading = true;
  data: any[];
  fileList: Array<object> = [];
  constructor() {}
  ngOnInit(): void {
    this.data = [];
    this.getData();
  }
  ngOnChanges() {
    //this.childFunction()
    this.getData();
  }

  getData(): void {
    const number = Math.floor(Math.random() * 100);
    this.data = [];
    this.data.push(this.File1Name);

    setTimeout(() => {
      this.displayData = [...this.data];
      this.loading = false;
    }, number);
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
      this.displayData = this.File1Name;
    }
  }
}
