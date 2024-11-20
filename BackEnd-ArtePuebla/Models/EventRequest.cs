namespace BackEnd_ArtePuebla.Models
{
    public class EventRequest
    {
        public string nameEvent {  get; set; }
        public string typeEvent { get; set; }
        public string startDate { get; set; }
        public string endDate { get; set; }
        public string startTime { get; set; }
        public string endTime { get; set; }
        public string address { get; set; }
        public string place { get; set; }
        public int cost { get; set; }
        public string publicType {  get; set; }
        public string description { get; set; }
    }
}
