const request = require('request')
const cheerio = require('cheerio')

// TODO refatorar em clase e metodo


function findAcao(codigo) {
    return new Promise((resolve, reject) => {
        request('https://statusinvest.com.br/acoes/' + codigo, (err, resp, body) => {
            try {
                const ch = cheerio.load(body)
                const preco = ch('#main-2 > div:nth-child(3) > div > div.pb-3.pb-md-5 > div > div.info.special.w-100.w-md-33.w-lg-20 > div > div:nth-child(1) > strong').text().trim().replace(',','.')        
                const empresa = ch('#company-section > div > div.d-block.d-md-flex.mb-5.img-lazy-group > div.company-description.w-100.w-md-70.ml-md-5 > h4 > span').text().trim()
                const setorNome = ch('#company-section > div > div.card.bg-main-gd-h.white-text.rounded > div > div:nth-child(1) > div > div > div > a > strong').text().trim()
                const subsetorNome = ch('#company-section > div > div.card.bg-main-gd-h.white-text.rounded > div > div.info.pl-md-2.pr-md-2 > div > div > div > a > strong').text().trim()
                const selectorSegmento = '#company-section > div > div.card.bg-main-gd-h.white-text.rounded > div > div:nth-child(3) > div > div > div >'
                const segmentoNome = ch(selectorSegmento + ' a > strong').text().trim()               
                const link = ch(selectorSegmento + ' a ').attr('href')      
                const arrayLink = link.split('/').filter(i => parseInt(i))

                const setor = {
                    'id':arrayLink[0],
                    'nome':setorNome
                }    
                
                const subsetor = {
                    'id':arrayLink[1],
                    'nome':subsetorNome
                }  

                const segmento = {
                    'id':arrayLink[2],
                    'nome':segmentoNome
                }  

                const image = ch('#company-section > div > div.d-block.d-md-flex.mb-5.img-lazy-group > div.company-brand.w-100.w-md-30.p-3.rounded.mb-3.mb-md-0.bg-lazy').attr('data-img')
                const id = image.match(/(\d+)/)[0]; 

                const result = {
                    id,
                    empresa,
                    preco,
                    setor,
                    subsetor,
                    segmento,
                }
                resolve(result)
            }
            catch (error) {
                reject(error)
            }
        })
    })
}
function findCotacao(codigo) {
    return new Promise((resolve, reject) => {
        request('https://statusinvest.com.br/acoes/' + codigo, (err, resp, body) => {
            try {
                const ch = cheerio.load(body)
                const preco = ch('#main-2 > div:nth-child(3) > div > div.pb-3.pb-md-5 > div > div.info.special.w-100.w-md-33.w-lg-20 > div > div:nth-child(1) > strong').text().trim().replace(',','.')                    
                resolve(preco)
            }
            catch (error) {
                reject(error)
            }
        })
    })
}
module.exports = {
    findAcao, findCotacao
}