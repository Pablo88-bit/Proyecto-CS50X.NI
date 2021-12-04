(function(){

    var ActualizarHora = function(){
        var fecha = new Date(),
            dia = fecha.getDate(),
            mes = fecha.getMonth(),
            year = fecha.getFullYear(),
            ampm,
            horas = fecha.getHours(),
            minutos = fecha.getMinutes(),
            segundos = fecha.getSeconds(),
            DiaSemana = fecha.getDay();


            var pDia = document.getElementById('dia'),
                pMes = document.getElementById('mes'),
                pYear = document.getElementById('year'),
                pAmpm = document.getElementById('ampm'),
                pHoras = document.getElementById('horas'),
                pMinutos = document.getElementById('minutos'),
                pSegundos = document.getElementById('segundos'),
                pDiaSemana = document.getElementById('diasemana');


            /*Fecha*/
            var Semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
            pDiaSemana.textContent = Semana[DiaSemana];

            PDia.textContent = dia;

            var Meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
            pMes.textContent = Meses[mes];

            pYear.textContet = year;


            /*Hora*/
            if(horas >= 12){
                horas = horas - 12;
                ampm = 'PM';
            }else
            {
                ampm = 'AM';
            }

            if(horas == 0){
                horas = 12;
            }

            if(minutos < 10){ minutos = "0" + minutos }
            if(segundos < 10){ segundos = "0" + segundos }

            pHoras.textContent = horas;
            pMinutos.textContent = minutos;
            pSegundos.textContent = segundos;
            pAmpm.textContent = ampm;

    };

    /*Para que se ejecute la función cada segundos*/
    ActualizarHora()
    var intervalo = setInterval(ActualizarHora, 1000);

}())