'use strict';
/**
 * 2-dars. Ma'lumotlardan hisobot tayyorlash: filter, map, reduce, sort
 * Ishga tushirish: node 02-malumot-hisobot.js
 */
const assert = require('node:assert/strict');

const orders = [
  { id: 1, customer: 'Anvar',   product: 'Daftar',  price: 5000,  qty: 10, status: 'paid' },
  { id: 2, customer: 'Dilnoza', product: 'Ruchka',  price: 2000,  qty: 25, status: 'paid' },
  { id: 3, customer: 'Anvar',   product: 'Kitob',   price: 45000, qty: 1,  status: 'paid' },
  { id: 4, customer: 'Jasur',   product: 'Daftar',  price: 5000,  qty: 4,  status: 'cancelled' },
  { id: 5, customer: 'Dilnoza', product: 'Daftar',  price: 5000,  qty: 6,  status: 'paid' },
  { id: 6, customer: 'Jasur',   product: 'Ruchka',  price: 2000,  qty: 5,  status: 'pending' },
];

const isPaid = (order) => order.status === 'paid';
const orderTotal = (order) => order.price * order.qty;

function totalRevenue(list) {
  return list.filter(isPaid).reduce((sum, order) => sum + orderTotal(order), 0);
}

function groupBy(items, getKey) {
  return items.reduce((groups, item) => {
    const key = getKey(item);
    (groups[key] ||= []).push(item);
    return groups;
  }, {});
}

function revenueByCustomer(list) {
  const groups = groupBy(list.filter(isPaid), (o) => o.customer);
  return Object.entries(groups)
    .map(([customer, items]) => ({ customer, orders: items.length, total: totalRevenue(items) }))
    .sort((a, b) => b.total - a.total);
}

function topProduct(list) {
  const qtyByProduct = {};
  for (const order of list.filter(isPaid)) {
    qtyByProduct[order.product] = (qtyByProduct[order.product] ?? 0) + order.qty;
  }
  const [product, qty] = Object.entries(qtyByProduct).sort((a, b) => b[1] - a[1])[0] ?? [null, 0];
  return { product, qty };
}

function countByStatus(list) {
  return list.reduce((acc, o) => ({ ...acc, [o.status]: (acc[o.status] ?? 0) + 1 }), {});
}

module.exports = { totalRevenue, groupBy, revenueByCustomer, topProduct, countByStatus };

if (require.main === module) {
  console.log('Jami tushum:', totalRevenue(orders), "so'm");
  console.log('Eng ko\'p sotilgan:', topProduct(orders));
  console.log('Holatlar:', countByStatus(orders));
  console.log('\nMijozlar reytingi:');
  console.table(revenueByCustomer(orders));

  assert.equal(totalRevenue(orders), 50000 + 50000 + 45000 + 30000);
  assert.deepEqual(topProduct(orders), { product: 'Ruchka', qty: 25 });
  assert.equal(revenueByCustomer(orders)[0].customer, 'Anvar');
  assert.deepEqual(countByStatus(orders), { paid: 4, cancelled: 1, pending: 1 });
  assert.equal(totalRevenue([]), 0);
  console.log('✓ Barcha tekshiruvlar o\'tdi');
}
