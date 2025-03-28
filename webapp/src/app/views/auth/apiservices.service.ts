import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class ApiservicesService {

  constructor(private api: HttpClient) { }



  loginOnSysteme(body:any){
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':'application/json',
        Authorization: ''
      })
    };
    return this.api.post('/api/authentication/',body, httpOptions)
  }
}




