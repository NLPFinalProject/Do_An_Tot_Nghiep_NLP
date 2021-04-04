import { Component, OnInit } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';

@Component({
  selector: 'app-diff-content',
  templateUrl: './diff-content.component.html',
  styleUrls: ['./diff-content.component.scss']
})
export class DiffContentComponent implements OnInit {
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  loading = true;
  data = [
    {
      name: 'Hoàn thiện các giải pháp QLNN đối với các hoạt động tôn giáo ở Việt Nam trong thời kỳ đổi mới.docx'
    },
    {
      name: 'Quản lý nhà nước đối với tập đoàn kinh tế tư nhân ở Việt Nam hiện nay.pdf'
    },
    {
      name: 'Quản lý nhà nước về văn thư, lưu trữ.docx'
    },
    {
      name: 'Quản lý nhà nước về quy hoạch xây dựng nông thôn mới.docx'
    },
    {
      name: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...'
    },
    {
      name: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...'
    },
    {
      name: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...'
    },
    {
      name: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...'
    }
  ];
  fileList: Array<object> = [];
  constructor(private messageService: MessageService) {}
  ngOnInit(): void {
    this.getData();
  }

  getData(): void {
    const number = Math.floor(Math.random() * 100);
    setTimeout(() => {
      this.displayData = [...this.data];
      this.loading = false;
    }, number);
  }
}
