import { Component, OnInit } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';
import { ScrollToService, ScrollToConfigOptions } from '@nicky-lenaers/ngx-scroll-to';
import { ViewportScroller } from '@angular/common';
@Component({
  selector: 'app-diff-content',
  templateUrl: './diff-content.component.html',
  styleUrls: ['./diff-content.component.scss'],
})
export class DiffContentComponent implements OnInit {
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData1: Array<object> = [];
  displayData2: Array<object> = [];
  loading = true;
  temp = [
    {
      data: 'Hoàn thiện các giải pháp QLNN đối với các hoạt động tôn giáo ở Việt Nam trong thời kỳ đổi mới.docx',
      xxx:"you die",
      id:"7"
    },
    {
      data: 'Quản lý nhà nước đối với tập đoàn kinh tế tư nhân ở Việt Nam hiện nay.pdf',
      xxx:"you die",
      id:"2"

    },
    {
      data: 'Quản lý nhà nước về văn thư, lưu trữ.docx',
      xxx:"you die",
      id:"2"
    },
    {
      data: 'Quản lý nhà nước về quy hoạch xây dựng nông thôn mới.docx',
      xxx:"you die",
      id:"2"
    },
    {
      data: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',xxx:"you die",
      id:"2"
    },
    {
      data: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',xxx:"you die",
      id:"1"
    },
    {
      data: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',xxx:"you die",
      id:"2"
    },
    {
      data: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',xxx:"you die",
      id:"2"
    },
  ];
  temp2 = [
   
    {
      data: 'Quản lý nhà nước đối với tập đoàn kinh tế tư nhân ở Việt Nam hiện nay.pdf',
      xxx:"you die",
      id:"2"

    },
    {
      data: 'Quản lý nhà nước về văn thư, lưu trữ.docx',
      xxx:"you die",
      id:"1"
    },
    {
      data: 'Quản lý nhà nước về quy hoạch xây dựng nông thôn mới.docx',
      xxx:"you die"
      ,
      id:"1"
    },
    {
      data: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',xxx:"you die",
      id:"1"
    },
    {
      data: 'Hoàn thiện các giải pháp QLNN đối với các hoạt động tôn giáo ở Việt Nam trong thời kỳ đổi mới.docx',
      xxx:"you die",
      id:"1"
    },
    {
      data: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',xxx:"you die",
      id:"7"
    },
    {
      data: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',xxx:"you die",
      id:"1"
    },
    {
      data: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...',xxx:"you die",
      id:"1"
    },
  ];
  fileList: Array<object> = [];
  constructor(private messageService: MessageService,
    private viewportScroller: ViewportScroller,
    private scrollToService: ScrollToService,) {}
  ngOnInit(): void {
    this.getData();
  }
  shouldHighlight(id:any)
  {
    //console.log("id is", id);
    if(id=="1")
    {
      console.log('true');
      return true;
    }
     console.log('false');
    return false;
    
  }
  triggerScrollTo(id: any) {
  
      const config: ScrollToConfigOptions = {
        target: id,
      };

      this.scrollToService.scrollTo(config);
    
  }
  
  getData(): void {
    const number = Math.floor(Math.random() * 100);
    setTimeout(() => {
      this.displayData1 = [...this.temp];
      this.displayData2 = [...this.temp2];
      this.loading = false;
    }, number);
  }
}
