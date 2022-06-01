rawData = """

 OKC Receptionist
 Kelsie Roberson 
 Greg Wagner 
 Toby Markovich 
 Jeremy Peters 
 Evan Sparkman 
 Counter 
 OKC Outside Sales Desk
 OKC Manager Billy Balak
 OKC Receiving
 OKC Shipping
 OKC Pres/CEO Harvey Sparkman
 OKC Shipping 2
 OKC Purchasing Ryan Sparkman
 OKC Counter #1
 OKC Counter #2
 OKC Counter #3
 OKC Counter #4
 OKC Scotty Sparkman office
 Queena Maghirang
 Chris Schuler 
 OKC Conference Room
 Haley Henson 
 OKC Design/Logistics Kristen
 Preston 
 Kari Reagan 
 Lee Curtis 
 Kailee Pierce 
 Emily Ingram 
 Christine Cataldo 
 Gabriela Coman 
 Arden Deramus 
 Building 2 Office 
 Dylan Sparkman 
 Rotary 
 Layflat Testing 
 Test Certs 
 OKC Machine Shop
 OKC DISOKC
 Robert Wilder 
 OKC Quality Mark Koldoff
 Ryan Seales 
 Chris Stogsdill 
 David Baum 
 Frank Valley 
 Turgut Eren 
 Break Room 
 Heather Prince 
 Vendor Donna 
 Mary Elsen 
 Bailey Jarvis 
 Christie Hoag 
 Brian Shafer 
 Paulina Leal 
 Brunielly Ruy 
 Huzaifa Rizwan
 Aakaash Soni
 Bldg 3 Conference Room
 JD Leonard 
 Keith Marshall
 OKC Temp
 Juan Ortiz 
 James Hatley 
 Calvin Hammond 
 Juan Ortiz 
 Inside Counter 
 Warehouse Counter 
 Shipping 
 Back Warehouse 
 Break Room 
 George Ruegg  
 Sales Office 
 Eugene Delarosa 
 Mobile Truck #1 
 FAX 
 Lidia Solis 
 Ryan Myers 
 Julie Quintero 
 Chris Galbreath 
 Laura Cox 
 Nick Elmer 
 Bob Terral 
 Troy Splichal 
 Quality 
 Ship/Rec 
 Front Counter 
 Break Room 
 FAX 
 Mike Lopez 
 Robby Reed 
 Dalton Howell / Front Counter 
 Garret Ramsey 
 Randy McGlothlin  
 Front Counter 
 WHSE Line #3 
 WHSE Line #1 
 WHSE Line #2 
 Odessa Test 
 FAX 
 ODE 
 Sammy 
 Counter Sales 
 Jeanell 
 Hydraulic 
 Industrial 
 Break Room 
1516
 Warehouse 1 
 Mailbox 
 FAX 
 ALI RINGER
 Cody Graham 
 Whse Counter #1 
 Whse Counter #2 
 Brandon Smith 
 Austin 
 FAX 
 VER RING
 Wacey Hurst 
 Cody Hurst 
 Inside Counter 
 Dan Miller 
 Counter #1 
 Counter #2 
 WHSE Line #1 
 WHSE Line #2 
1718
 FAX 
 FWW 
 Heath Hancock 
 Josh Wedding 
 Damon Woody 
 Aaron Homer 
 Webb Mosley 
 Luke Hughes 
 KIL Shipping 
 File Room 
 KIL WHSE 
 WHSE Phone #1 
 FAX 
 Bill Sabo 
 Jimmy Cole 
 Anthony Ianni 
 Front Counter 
 Andrew Prichard 
 Richard Kohl 
 David Burwell 
 Conference Room 
 WHSE LINE 1 
 WHSE #2 
 WHSE #3 
 Mobile Truck #3 
 FAX 
 Andy Beaty 
 OPEN Office 
 Counter #1 
 Counter #2 
 Counter #3 
 WHSE Phone #1 
 WHSE Phone #2 
 WHSE Phone #3 
 FAX 
 FWE RING
2110
2111
2112
2113
2114
2115
2116
2117
2118
2119
2120
2121
 FAX 
 WIL 
 Office 
 Sales Counter 
 Ryan Benoit 
 Hydraulic Area 
 Pump Area 
 FAX 
2410
 Anthony Pena 
 Lee Rater 
 John Aguilar
 Mike Canon 
 Mike office 
 FAX 
 SAN RINGER
2510
2511
2512
2513
2514
2515
2516
2517
 FAX 
 GRE RINGER
 David Mclaughlin 
 Kyle Bookout 
 El Reno Counter 
 Hydraulic Repair 
 FAX 
 Clay 
 Inside Sales #1 
 Inside Sales #2 
 Carlos Aguilar 
 Whse Counter #1 
 Whse Counter #2 
 Dylan Mooney 
 Jared Yap 
 Outside Sales 
 FAX 
 Hobbs 
 Walkin Counter 
 Hobbs Office
 Dustin Office 
 Hallway Office 
 Warehouse Phone #1 
 WHSE Phone #2 
 WHSE Phone #3 
 FAX 
 HOB
 Raul 
 Victoria Barrera  
 Counter #1 
 Counter #2 
 Conference Room 
 Break Room 
 Mandi Mercer 
 Ryan Myers 
 FAX 
 POM PAGE 2
 Dan 
 Rick 
 Counter 
 Wayne Sapp 
 Adam Shuck 
 WHSE #1 
 WHSE #2 
 Counter 
 Wayne Hankins 
 FAX 
 LAK RING
 Chris Luba 
 Rocco Mook 
 Mark Lockhart 
 Brad / MFG Office 
 Kyle Stine 
 Quality Assurance 
 Conference Room 
 Front Office 
 Lobby 
 Test Bunker 
 WHSE Station 
 Maint. 
 West Bunker 
 COR
 Cody 
 Jacob Graham 
 Brayden Ogilvie 
 Warehouse Counter 
 Back Warehouse 
 Victor Miller 
 Cory Lewis 
 Tony Robinson 
 WHSE Line 1 
 WHSE Line 2 
 FAX 
 SLC RINGER
 Victor Berrios 
 Counter Sales 
 Jerry Harris 
 Conference Room 
 WHSE #1 
 WHSE #2 
 POM PAGE 2
3510
3511
3512
3513
3514
3515
 Tim Cryer
 Ryan Benoit 
 SULFUR RING
 Charlotte Store 
 Charlotte Store 
 Charlotte Store 
 Charlotte Counter 
 Charlotte Store 
 WHSE #2 
 Elrad Cuellar 
 Cris Acosta 
 Counter Sales 
 Shipping 
 Inside Sales 
 Inside Sales 
 Inside Sales 
 Break Room 

"""

for line in rawData.splitlines():
    print(line.strip())